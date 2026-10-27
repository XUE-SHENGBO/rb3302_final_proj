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
from geometry_msgs.msg import PoseStamped, Twist
from nav2_msgs.action import NavigateToPose
from nav2_simple_commander.robot_navigator import BasicNavigator
from nav_msgs.msg import Odometry
import rclpy
from rclpy.duration import Duration
from rclpy.parameter import Parameter
from rclpy.qos import qos_profile_sensor_data
from rclpy.signals import SignalHandlerOptions
from rclpy.time import Time
from std_srvs.srv import Trigger
from tf2_ros import Buffer, TransformException, TransformListener


class MissionExpired(RuntimeError):
    """The entire round has consumed its time budget."""


class GoalFailed(RuntimeError):
    """One visit failed and may be retried under the configured policy."""


class MissionManager(BasicNavigator):
    """Own one ordered mission; preparation never starts robot motion."""

    def __init__(self):
        super().__init__(node_name='mission_manager')
        share = Path(get_package_share_directory('competition_manager'))
        defaults = {
            'goals': '', 'required_goal_count': 4,
            'landmarks_file': str(share / 'config/landmarks.yaml'),
            'map_frame': 'map', 'base_frame': 'base_link', 'odom_topic': '/odom',
            'set_initial_pose': False, 'initial_letter': '', 'initial_heading': '',
            'start_automatically': False, 'validate_only': False,
            'mission_timeout_sec': 180.0, 'goal_timeout_sec': 60.0,
            'dwell_sec': 3.0, 'arrival_timeout_sec': 15.0,
            'arrival_tolerance': 0.08, 'stopped_linear_tolerance': 0.02,
            'stopped_angular_tolerance': 0.05, 'telemetry_timeout_sec': 0.5,
            'tf_timeout_sec': 1.0, 'goal_heading_mode': 'approach',
            'fixed_goal_yaw': 0.0, 'max_retries': 1, 'failure_policy': 'stop',
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
        self._stop_pub = self.create_publisher(Twist, '/cmd_vel', 10)
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
                     'stopped_angular_tolerance', 'telemetry_timeout_sec', 'tf_timeout_sec'):
            positive(self.p(name), name)
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
        while not self._start_requested.is_set():
            self._spin()
        self._ready = False
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

    def _navigate(self, target):
        goal_deadline = min(self._deadline, time.monotonic() + self.p('goal_timeout_sec'))
        while not self.nav_to_pose_client.server_is_ready():
            self._spin()
            if time.monotonic() >= goal_deadline:
                raise GoalFailed('Navigation action server unavailable')
        self._cancel_requested = False
        self.goal_handle = None
        self.result_future = None
        goal = NavigateToPose.Goal()
        goal.pose = self.make_pose(target)
        self._send_future = self.nav_to_pose_client.send_goal_async(goal)
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
        if result.status != GoalStatus.STATUS_SUCCEEDED:
            raise GoalFailed(f'Nav2 goal failed with status {result.status}')

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

    def _dwell(self, target):
        window = StopWindow(self.p('dwell_sec'))
        expires = time.monotonic() + self.p('arrival_timeout_sec')
        while True:
            self._check_deadline()
            self._stop_pub.publish(Twist())
            pose = self._current_pose()
            inside = (pose is not None and math.hypot(pose[0] - target[0], pose[1] - target[1])
                      <= self.p('arrival_tolerance'))
            now = time.monotonic()
            if window.update(now, inside and self._stationary()):
                return
            if now >= expires:
                raise GoalFailed('Could not verify position and uninterrupted stationary dwell')
            self._spin()

    def run_mission(self):
        """Prepare, start explicitly, visit in order and retain recoverable results."""
        route, positions, initial = self._validate()
        if self.p('validate_only'):
            self.get_logger().info(
                f'Configuration valid: route={route}, landmarks={len(positions)}')
            return True
        if initial is not None:
            self._explicit_initial_pose = True
            self.setInitialPose(self.make_pose(initial))
        self.get_logger().info('Waiting for Nav2 and AMCL; set the actual pose in RViz.')
        self.waitUntilNav2Active()
        while self._current_pose() is None or not self._stationary():
            self._spin()
        self._wait_for_start()
        for index, visit in enumerate(self._state['visits']):
            if visit['status'] in ('completed', 'skipped'):
                continue
            for attempt in range(self.p('max_retries') + 1):
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
                    self._navigate(target)
                    visit['status'] = 'dwelling'
                    self._record('dwelling')
                    self._dwell(target)
                except GoalFailed as error:
                    visit.update(status='failed', reason=str(error))
                    self.get_logger().warning(str(error))
                    if not self.stop_task():
                        raise RuntimeError('Cancellation unconfirmed; refusing another goal')
                    self._check_deadline()
                    self._record('running')
                    if attempt < self.p('max_retries'):
                        continue
                    if self.p('failure_policy') == 'skip':
                        visit['status'] = 'skipped'
                        self._record('running')
                        break
                    self._record('failed')
                    return False
                else:
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
