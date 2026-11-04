"""Run an explicitly started, timed landmark mission with measured stops."""

import fcntl
import json
import math
import os
from pathlib import Path
import signal
import sys
import threading
import time

from action_msgs.msg import GoalStatus
from ament_index_python.packages import get_package_share_directory
from competition_manager.mission_rules import (
    approach_heading, initial_coordinates, load_landmarks, parse_route, positive,
    read_checkpoint, StopWindow, write_checkpoint,
)
from competition_manager.localization_guard import DEFAULTS as LOCALIZATION_DEFAULTS, LocalizationGuard
from geometry_msgs.msg import PoseStamped, Twist
from lifecycle_msgs.srv import GetState
from nav2_msgs.action import NavigateToPose
from nav2_simple_commander.robot_navigator import BasicNavigator
from nav_msgs.msg import Odometry
import rclpy
from rclpy.duration import Duration
from rclpy.parameter import Parameter
from rclpy.qos import qos_profile_sensor_data
from rclpy.signals import SignalHandlerOptions
from rclpy.time import Time
from std_srvs.srv import Empty, Trigger
from tf2_ros import Buffer, TransformException, TransformListener


class MissionExpired(RuntimeError):
    """The entire round has consumed its time budget."""


class GoalFailed(RuntimeError):
    """One visit failed and may be retried under the configured policy."""


class MissionManager(LocalizationGuard, BasicNavigator):
    """Own one ordered mission; preparation never starts robot motion."""

    def __init__(self):
        super().__init__(node_name='mission_manager')
        share = Path(get_package_share_directory('competition_manager'))
        defaults = {
            **LOCALIZATION_DEFAULTS,
            'goals': '', 'required_goal_count': 4,
            'landmarks_file': str(share / 'config/landmarks.yaml'),
            'map_frame': 'map', 'base_frame': 'base_link', 'odom_topic': '/odom',
            'set_initial_pose': False, 'initial_letter': '', 'initial_heading': '',
            'start_automatically': False, 'validate_only': False,
            'mission_timeout_sec': 6000.0, 'goal_timeout_sec': 1200.0,
            'dwell_sec': 3.0, 'arrival_timeout_sec': 15.0,
            'arrival_tolerance': 0.10, 'stopped_linear_tolerance': 0.02,
            'stopped_angular_tolerance': 0.05, 'telemetry_timeout_sec': 0.5,
            'tf_timeout_sec': 1.0, 'goal_heading_mode': 'approach',
            'fixed_goal_yaw': 0.0, 'max_retries': 5, 'failure_policy': 'stop',
            'retry_delay_sec': 1.0,
            'resume_file': '',
            'result_file': str(Path.home() / '.ros/rb3302/last_mission.json'),
        }
        for name, value in defaults.items():
            self.declare_parameter(name, value)
        self.declare_parameter('initial_pose', Parameter.Type.DOUBLE_ARRAY)
        self._explicit_initial_pose = False
        self._ready = False
        self._start_requested = threading.Event()
        self._deadline = None
        self._task_active = False
        self._send_future = None
        self._cancel_requested = False
        self._odom_sample = None
        self._state = None
        self._result_path = None
        self._tf = Buffer(cache_time=Duration(seconds=10.0))
        self._tf_listener = TransformListener(self._tf, self)
        self.create_subscription(
            Odometry, self.p('odom_topic'), self._odom_callback, qos_profile_sensor_data)
        self._stop_pub = self.create_publisher(Twist, '/cmd_vel_stop', 10)
        self._init_localization()
        self.create_service(Trigger, '/mission_manager/start', self._start_callback)
        self.create_service(Trigger, '/mission_manager/status', self._status_callback)

    def p(self, name):
        """Return a declared parameter value."""
        return self.get_parameter(name).value

    def _odom_callback(self, msg):
        self._odom_sample = (time.monotonic(), msg.twist.twist)

    def _start_callback(self, request, response):
        del request
        response.success = self._ready and self._deadline is None
        if response.success:
            self._start_requested.set()
        response.message = (
            'Start accepted' if response.success else 'Mission is not ready to start')
        return response

    def _status_callback(self, request, response):
        del request
        response.success = True
        response.message = json.dumps({
            'ready': self._ready,
            'remaining_sec': max(0.0, self._deadline - time.monotonic())
            if self._deadline is not None else None,
            'mission': self._state,
        }, ensure_ascii=False)
        return response

    def _waitForNodeToActivate(self, node_name):
        """Retry lost lifecycle replies without limiting preparation time."""
        service = f'{node_name}/get_state'
        while True:
            client = self.create_client(GetState, service)
            try:
                while not client.wait_for_service(timeout_sec=1.0):
                    self._spin()
                    self.get_logger().info(f'{service} service not available, waiting...')
                future = client.call_async(GetState.Request())
                response_deadline = time.monotonic() + 5.0
                while not future.done() and time.monotonic() < response_deadline:
                    self._spin()
                if not future.done():
                    client.remove_pending_request(future)
                    future.cancel()
                    self.get_logger().warning(
                        f'{service} response timed out; retrying. Preparation remains waiting.')
                    continue
                try:
                    response = future.result()
                except Exception as error:
                    self.get_logger().warning(f'{service} request failed: {error}; retrying.')
                    response = None
                if response is not None and response.current_state.label == 'active':
                    self.get_logger().info(f'{node_name} is active.')
                    return
            finally:
                self.destroy_client(client)
            retry_at = time.monotonic() + 1.0
            while time.monotonic() < retry_at:
                self._spin()

    def _waitForInitialPose(self):
        """Preserve RViz localization unless numeric initialization was requested."""
        if self._explicit_initial_pose:
            return super()._waitForInitialPose()
        self.get_logger().info('Waiting for AMCL pose; preserving RViz initialization.')
        while not self.initial_pose_received:
            self._spin()

    def _spin(self, seconds=0.05, check_deadline=True):
        if not rclpy.ok():
            raise RuntimeError('ROS shut down')
        if check_deadline:
            self._check_deadline()
        rclpy.spin_once(self, timeout_sec=seconds)
        if check_deadline:
            self._check_deadline()

    def _check_deadline(self):
        if self._deadline is not None and time.monotonic() >= self._deadline:
            self._stop_pub.publish(Twist())
            raise MissionExpired('Entire mission time limit reached')

    def make_pose(self, coordinates):
        """Create a map-frame pose with normalized yaw quaternion."""
        x, y, yaw = coordinates
        pose = PoseStamped()
        pose.header.frame_id = self.p('map_frame')
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x, pose.pose.position.y = float(x), float(y)
        pose.pose.orientation.z, pose.pose.orientation.w = math.sin(yaw / 2), math.cos(yaw / 2)
        return pose

    def _current_pose(self):
        try:
            tf = self._tf.lookup_transform(self.p('map_frame'), self.p('base_frame'), Time())
            age = (self.get_clock().now() - Time.from_msg(tf.header.stamp)).nanoseconds / 1e9
            if age > self.p('tf_timeout_sec') or age < -2.0:
                return None
            q, t = tf.transform.rotation, tf.transform.translation
            yaw = math.atan2(2 * (q.w * q.z + q.x * q.y), 1 - 2 * (q.y * q.y + q.z * q.z))
            pose = (t.x, t.y, yaw)
            return pose if all(math.isfinite(v) for v in pose) else None
        except TransformException:
            return None

    def _stationary(self):
        if self._odom_sample is None:
            return False
        stamp, velocity = self._odom_sample
        return (time.monotonic() - stamp <= self.p('telemetry_timeout_sec')
                and math.hypot(velocity.linear.x, velocity.linear.y)
                <= self.p('stopped_linear_tolerance')
                and abs(velocity.angular.z) <= self.p('stopped_angular_tolerance'))

    def _validate(self):
        for name in ('mission_timeout_sec', 'goal_timeout_sec', 'arrival_timeout_sec',
                     'arrival_tolerance', 'stopped_linear_tolerance',
                     'stopped_angular_tolerance', 'telemetry_timeout_sec', 'tf_timeout_sec',
                     'retry_delay_sec'):
            positive(self.p(name), name)
        for name in LOCALIZATION_DEFAULTS:
            positive(self.p(name), name)
        for name in ('localization_max_updates', 'localization_stable_samples'):
            if type(self.p(name)) is not int or self.p(name) < 3:
                raise ValueError(f'{name} must be an integer >= 3')
        if self.p('localization_min_match_ratio') > 1:
            raise ValueError('localization_min_match_ratio must be <= 1')
        positive(self.p('dwell_sec'), 'dwell_sec', minimum=3.0)
        if self.p('arrival_timeout_sec') < self.p('dwell_sec'):
            raise ValueError('arrival_timeout_sec must be >= dwell_sec')
        if self.p('max_retries') < 0 or self.p('max_retries') > 5:
            raise ValueError('max_retries must be between 0 and 5')
        if self.p('failure_policy') not in ('stop', 'skip'):
            raise ValueError('failure_policy must be stop or skip')
        if self.p('goal_heading_mode') not in ('approach', 'fixed'):
            raise ValueError('goal_heading_mode must be approach or fixed')
        if not math.isfinite(self.p('fixed_goal_yaw')):
            raise ValueError('fixed_goal_yaw must be finite')
        positions, north, digest = load_landmarks(self.p('landmarks_file'), self.p('map_frame'))
        route_value = self.p('goals')
        if self.p('resume_file') and not route_value:
            route_value = json.loads(Path(self.p('resume_file')).expanduser().read_text())['route']
        route = parse_route(route_value, positions, self.p('required_goal_count'))
        self._result_path = self.p('resume_file') or self.p('result_file')
        if self.p('resume_file'):
            self._state = read_checkpoint(
                self.p('resume_file'), route, digest, self.p('mission_timeout_sec'))
        else:
            self._state = {
                'version': 1, 'route': route, 'landmarks_sha256': digest,
                'mission_timeout_sec': self.p('mission_timeout_sec'),
                'started_at_unix': None, 'status': 'preparing',
                'visits': [{'letter': letter, 'status': 'pending'} for letter in route],
            }
        initial = None
        if self.p('initial_letter'):
            if self.p('set_initial_pose'):
                raise ValueError('Choose initial_letter OR set_initial_pose, not both')
            initial = initial_coordinates(
                self.p('initial_letter'), self.p('initial_heading'), positions, north)
        elif self.p('set_initial_pose'):
            values = self.p('initial_pose')
            if len(values) != 3 or not all(math.isfinite(v) for v in values):
                raise ValueError('initial_pose must contain exactly [x, y, yaw]')
            initial = tuple(values)
        elif self.p('initial_heading'):
            raise ValueError('initial_heading requires initial_letter')
        return route, positions, initial

    def _record(self, status):
        self._state['status'] = status
        if self._deadline is not None:
            self._state['elapsed_sec'] = max(
                0.0, self.p('mission_timeout_sec') - (self._deadline - time.monotonic()))
        write_checkpoint(self._result_path, self._state)

    def _wait_for_start(self):
        self._ready = True
        self.get_logger().info(
            'READY: press Enter to START, or call /mission_manager/start. Timer has not started.')
        if sys.stdin.isatty():
            def read_start():
                if sys.stdin.readline():
                    self._start_requested.set()
            threading.Thread(target=read_start, daemon=True).start()
        if self.p('start_automatically'):
            self._start_requested.set()
        next_observation = time.monotonic()
        observation_interval = min(self.p('localization_update_interval_sec'),
                                   self.p('localization_pose_timeout_sec')/2)
        while not self._start_requested.is_set():
            if time.monotonic() >= next_observation and self._stationary():
                # AMCL normally stops publishing poses when odometry is still.
                # Keep observations fresh without resetting verification history
                # or clearing maps for a healthy, unchanged stationary estimate.
                self._localization_service(Empty, '/request_nomotion_update',
                                           time.monotonic()+0.5)
                next_observation = time.monotonic()+observation_interval
            self._spin()
            if not self._localization_quality()[0]:
                self._ready = False
                self.recover_localization()
                self._ready = True
                next_observation = time.monotonic()
        self._ready = False
        self.recover_localization()
        if self._current_pose() is None or not self._stationary():
            raise RuntimeError('Start rejected: need fresh TF and stationary odometry')
        now = time.monotonic()
        old_start = self._state['started_at_unix']
        if old_start is None:
            self._state['started_at_unix'] = time.time()
            remaining = self.p('mission_timeout_sec')
        else:
            elapsed = time.time() - old_start
            if elapsed < 0:
                raise ValueError('Clock moved backwards; refusing to reset resumed mission timer')
            remaining = self.p('mission_timeout_sec') - elapsed
        self._deadline = now + remaining
        self._check_deadline()
        self._record('running')
        self.get_logger().info(f'MISSION START: {remaining:.1f} seconds remaining')

    def _accept_goal(self, future):
        if self.goal_handle is not None:
            return
        handle = future.result()
        if handle is not None and handle.accepted:
            self.goal_handle = handle
            self._task_active = True
            self.result_future = handle.get_result_async()
            if self._cancel_requested:
                handle.cancel_goal_async()

    def _navigate(self, target):# handle sending goal
        goal_deadline = min(self._deadline, time.monotonic() + self.p('goal_timeout_sec'))
        while not self.nav_to_pose_client.server_is_ready():
            self._spin()
            if time.monotonic() >= goal_deadline:
                raise GoalFailed('Navigation action server unavailable')
        self._cancel_requested = False
        self.goal_handle = None
        self.result_future = None
        goal = NavigateToPose.Goal()#create a goal
        goal.pose = self.make_pose(target)#load target
        self._send_future = self.nav_to_pose_client.send_goal_async(goal)#send to action server
        self._send_future.add_done_callback(self._accept_goal)
        while not self._send_future.done() or self.goal_handle is None:
            self._spin()
            if self._send_future.done() and not self._send_future.result().accepted:
                self._send_future = None
                raise GoalFailed('Navigation goal rejected')
            if time.monotonic() >= goal_deadline:
                raise GoalFailed('Navigation goal acceptance timed out')
        self._send_future = None
        while not self.result_future.done():
            self._spin()
            if time.monotonic() >= goal_deadline:
                raise GoalFailed('Per-goal time limit reached')
        self._check_deadline()
        self._task_active = False
        result = self.result_future.result()
        details = (f'status={result.status}, '
                   f'error_code={getattr(result.result, "error_code", "unavailable")}, '
                   f'error_msg={getattr(result.result, "error_msg", "unavailable")!r}, '
                   f'target={target}, current_pose={self._current_pose()}')
        self.get_logger().info('Nav2 result: ' + details)
        if result.status != GoalStatus.STATUS_SUCCEEDED:
            raise GoalFailed('Nav2 goal failed: ' + details)

    def stop_task(self):
        """Cancel owned actions and publish zeros while waiting for termination."""
        self._cancel_requested = True
        end = time.monotonic() + 5.0
        cancel_sent = False
        while rclpy.ok() and time.monotonic() < end:
            self._stop_pub.publish(Twist())
            if self._send_future is not None and self._send_future.done():
                self._accept_goal(self._send_future)
                self._send_future = None
            if self.goal_handle is not None and self._task_active and not cancel_sent:
                self.goal_handle.cancel_goal_async()
                cancel_sent = True
            pending = self._send_future is not None and not self._send_future.done()
            active = self._task_active and self.result_future is not None
            if not pending and (not active or self.result_future.done()):
                self._task_active = False
                return True
            self._spin(check_deadline=False)
        return not self._task_active and self._send_future is None

    def _wait_before_retry(self):
        """Stay stopped while processing telemetry; charge waiting to the round."""
        delay = self.p('retry_delay_sec')
        self.get_logger().info(f'Navigation retry: staying stopped for {delay:.1f}s')
        until = time.monotonic() + delay
        while time.monotonic() < until:
            self._check_deadline()
            self._stop_pub.publish(Twist())
            self._spin()
        self._check_deadline()

    def _dwell(self, target):
        window = StopWindow(self.p('dwell_sec'))
        expires = time.monotonic() + self.p('arrival_timeout_sec')
        previous = None
        outside_since = None
        while True:
            self._check_deadline()
            self._stop_pub.publish(Twist())
            pose = self._current_pose()
            distance = (math.hypot(pose[0] - target[0], pose[1] - target[1])
                        if pose is not None else None)
            inside = distance is not None and distance <= self.p('arrival_tolerance')
            stationary = self._stationary()
            now = time.monotonic()
            conditions = (inside, stationary)
            if conditions != previous:
                error = f'{distance:.3f}m' if distance is not None else 'stale TF'
                self.get_logger().info(
                    f'Dwell conditions: position_error={error}, inside={inside}, '
                    f'stationary={stationary}; require continuous {self.p("dwell_sec")}s')
                previous = conditions
            # Nav2's success pose and the next AMCL/TF sample can straddle
            # the same 10 cm boundary. Retry promptly instead of idling 15 s.
            outside_since = (outside_since if outside_since is not None else now) if (
                distance is not None and not inside and stationary) else None
            if outside_since is not None and now - outside_since >= .5:
                raise GoalFailed(
                    f'Could not verify arrival within {self.p("arrival_tolerance"):.3f}m: {distance:.3f}m; '
                    'requesting navigation retry')
            if window.update(now, inside and stationary):
                return
            if now >= expires:
                position = (f'{distance:.3f}m (limit {self.p("arrival_tolerance"):.3f}m)'
                            if distance is not None else 'unavailable/stale TF')
                raise GoalFailed(
                    'Could not verify position and uninterrupted stationary dwell: '
                    f'position_error={position}, stationary={stationary}')
            self._spin()

    def wait_for_velocity_guard(self):
        """Do not start a mission against the old unguarded navigation launch."""
        while True:
            client = self.create_client(Trigger, '/velocity_guard/ready')
            try:
                if not client.wait_for_service(timeout_sec=1.0):
                    self.get_logger().info('Waiting for velocity_guard; restart start2.sh after upgrade.')
                    continue
                future = client.call_async(Trigger.Request())
                expires = time.monotonic() + 2.0
                while not future.done() and time.monotonic() < expires:
                    self._spin()
                if future.done() and future.result() is not None and future.result().success:
                    return
                if not future.done():
                    client.remove_pending_request(future)
                    future.cancel()
                self.get_logger().info('Waiting for velocity_guard with fresh scan and TF.')
                self._spin(1.0)
            finally:
                self.destroy_client(client)

    def run_mission(self):
        """Prepare, start explicitly, visit in order and retain recoverable results."""
        route, positions, initial = self._validate()
        self.get_logger().info(
            f'Mission limits: total={self.p("mission_timeout_sec"):.1f}s, '
            f'per attempt={self.p("goal_timeout_sec"):.1f}s; timer starts after READY.')
        if self.p('validate_only'):
            self.get_logger().info(
                f'Configuration valid: route={route}, landmarks={len(positions)}')
            return True
        if initial is not None:
            self._explicit_initial_pose = True
            self.setInitialPose(self.make_pose(initial))
        self.get_logger().info('Waiting for Nav2 and AMCL; set the actual pose in RViz.')
        self.waitUntilNav2Active()
        self.wait_for_velocity_guard()
        while self._current_pose() is None or not self._stationary():
            self._spin()
        self.recover_localization(force=True)
        self._wait_for_start()
#==============================================================================================================
        for index, visit in enumerate(self._state['visits']):                                     # for each goal point
            #index: the index of goal points from 0
            #visit: dic:{'letter': 'A', 'status': 'pending'}
            if visit['status'] in ('completed', 'skipped'):
                continue
            for attempt in range(self.p('max_retries') + 1):# retires
                self._check_deadline()
                current = self._current_pose()
                if current is None:
                    raise RuntimeError('Lost fresh map-to-base transform')
                xy = positions[visit['letter']]
                yaw = (approach_heading(current, xy) if self.p('goal_heading_mode') == 'approach'
                       else self.p('fixed_goal_yaw'))
                target = (*xy, yaw)
                visit.update(status='moving', attempt=attempt + 1, target=list(target))
                self._record('running')
                self.get_logger().info(
                    f'Goal {index + 1}/{len(route)} {visit["letter"]}, attempt {attempt + 1}')
                try:
                    navigation_target = target
                    if attempt > 0:
                        # Put the retry's acceptance disk farther toward the true
                        # centre. Verification always uses the ORIGINAL landmark.
                        dx, dy = xy[0] - current[0], xy[1] - current[1]
                        distance = math.hypot(dx, dy)
                        if 0.01 < distance <= 2 * self.p('arrival_tolerance'):
                            margin = min(.03, self.p('arrival_tolerance') / 2)
                            navigation_target = (xy[0] + margin * dx / distance,
                                                 xy[1] + margin * dy / distance, yaw)
                    self._navigate(navigation_target) # send to navigation function on top and wait until the nav2 action returns a result
                    visit['status'] = 'dwelling'
                    self._record('dwelling')
                    self._dwell(target)
                except GoalFailed as error:                                                        # catch error
                    visit.update(status='failed', reason=str(error))# handle error
                    self.get_logger().warning(str(error))
                    if not self.stop_task():
                        raise RuntimeError('Cancellation unconfirmed; refusing another goal')
                    self._check_deadline()
                    self._record('running')
                    if attempt < self.p('max_retries'):
                        self.recover_localization()
                        self._wait_before_retry()
                        continue
                    if self.p('failure_policy') == 'skip':
                        visit['status'] = 'skipped'
                        self._record('running')
                        break
                    self._record('failed')
                    return False
                else:# marked as completed
                    visit.pop('reason', None)
                    visit['status'] = 'completed'
                    self._record('running')
                    self.get_logger().info(
                        f'Goal {index + 1} reached; stop >= {self.p("dwell_sec")}s')
                    break
        self._check_deadline()
        complete = all(v['status'] == 'completed' for v in self._state['visits'])
        self._record('completed' if complete else 'partial')
        self.get_logger().info(
            ('All goals reached in order' if complete else 'Route ended with skipped goals')
            + f'; elapsed={self._state["elapsed_sec"]:.2f}s; result={self._result_path}')
        return complete
#===================================================================================================================

def main(args=None):
    """Run one mission per ROS domain and always cancel on abnormal termination."""
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)

    def interrupted(signum, frame):
        del signum, frame
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGHUP, interrupted)
    navigator = None
    lock = None
    code = 1
    try:
        lock_path = Path.home() / '.ros/rb3302' / (
            'mission-domain-' + os.environ.get('ROS_DOMAIN_ID', '0') + '.lock')
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock = lock_path.open('a')
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        navigator = MissionManager()
        code = 0 if navigator.run_mission() else 1
    except KeyboardInterrupt:
        code = 130
        if navigator and navigator._deadline is not None:
            navigator._record('interrupted')
    except Exception as error:
        if navigator:
            navigator.get_logger().error(f'Mission stopped: {error}')
            if navigator._state is not None and navigator._deadline is not None:
                navigator._record('timed_out' if isinstance(error, MissionExpired) else 'failed')
        else:
            print(f'Mission setup failed: {error}')
    finally:
        if navigator:
            try:
                if rclpy.ok() and navigator._deadline is not None:
                    if not navigator.stop_task():
                        navigator.get_logger().error('Action cancellation was not confirmed')
            finally:
                navigator.destroy_node()
        if lock:
            lock.close()
        if rclpy.ok():
            rclpy.shutdown()
    return code


if __name__ == '__main__':
    raise SystemExit(main())
