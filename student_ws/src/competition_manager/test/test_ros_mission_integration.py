"""Opt-in ROS action integration on an isolated domain, never physical hardware."""

import os
import math
from pathlib import Path
import sys
import threading
import time

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
from competition_manager import mission_manager as runtime  # noqa: E402, I100
from geometry_msgs.msg import PoseWithCovarianceStamped, TransformStamped, Twist  # noqa: E402
from nav2_msgs.action import NavigateToPose  # noqa: E402
from nav_msgs.msg import OccupancyGrid, Odometry  # noqa: E402
from sensor_msgs.msg import LaserScan
from nav2_msgs.srv import ClearEntireCostmap
from rclpy.qos import DurabilityPolicy, QoSProfile
import rclpy  # noqa: E402
from rclpy.action import ActionServer, CancelResponse, GoalResponse  # noqa: E402
from rclpy.callback_groups import ReentrantCallbackGroup  # noqa: E402
from rclpy.executors import MultiThreadedExecutor  # noqa: E402
from rclpy.node import Node  # noqa: E402
from std_srvs.srv import Empty, Trigger
from tf2_ros import TransformBroadcaster  # noqa: E402


pytestmark = pytest.mark.skipif(
    os.environ.get('RB3302_ROS_INTEGRATION') != '1', reason='Isolated ROS integration is opt-in')


def test_default_parameters_validate_without_navigation(tmp_path, monkeypatch):
    """Exercise declared defaults, which mission-logic fixtures override."""
    assert os.environ.get('ROS_DOMAIN_ID') == '217'
    assert os.environ.get('ROS_AUTOMATIC_DISCOVERY_RANGE') == 'LOCALHOST'
    package = Path(__file__).parents[1]
    monkeypatch.setattr(runtime, 'get_package_share_directory', lambda _: str(package))
    rclpy.init(args=[
        '--ros-args', '-p', 'goals:=\"BABA\"', '-p', 'validate_only:=true',
        '-p', f'result_file:={tmp_path / "result.json"}',
    ])
    node = None
    try:
        node = runtime.MissionManager()
        assert node.run_mission()
        assert node._deadline is None
        assert not node._task_active
        assert not (tmp_path / 'result.json').exists()
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.shutdown()


class FakeNavigation(Node):
    """Publish synthetic pose/odometry and implement only the navigation action."""

    def __init__(self, block=False, delay=0, fail_first=False):
        super().__init__('fake_navigation')
        self.create_service(Trigger, '/velocity_guard/ready', self.guard_ready)
        self.position = [0., 0., 0., 1.]
        self.block, self.delay = block, delay
        self.accept_release = threading.Event()
        self.visits = []
        self.cancellations = 0
        self.zeros = 0
        self.fail_first = fail_first
        self.degraded = False
        self.refinements = 0
        self.events = []
        group = ReentrantCallbackGroup()
        self.create_service(Empty, '/request_nomotion_update', self.refine, callback_group=group)
        for prefix in ('global', 'local'):
            self.create_service(ClearEntireCostmap,
                f'/{prefix}_costmap/clear_entirely_{prefix}_costmap',
                lambda req, res, label=prefix: self.clear(label, res), callback_group=group)
        self.tf = TransformBroadcaster(self)
        self.odom = self.create_publisher(Odometry, '/odom', 10)
        self.amcl = self.create_publisher(PoseWithCovarianceStamped, '/amcl_pose', QoSProfile(
            depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL))
        self.scan = self.create_publisher(LaserScan, '/scan', 10)
        self.map_pub = self.create_publisher(OccupancyGrid, '/map', QoSProfile(
            depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL))
        grid = OccupancyGrid()
        grid.header.frame_id = 'map'
        grid.info.resolution = .1
        grid.info.width = grid.info.height = 100
        grid.info.origin.position.x = grid.info.origin.position.y = -5.
        grid.info.origin.orientation.w = 1.
        grid.data = [100 if x in (0,99) or y in (0,99) else 0
                     for y in range(100) for x in range(100)]
        self.map_pub.publish(grid)
        # Serialize the sensor callback and use 10 Hz; overlapping Python sensor
        # callbacks can starve TF delivery and make this fixture itself unhealthy.
        self.create_timer(.1, self.publish_pose)
        self.create_subscription(Twist, '/cmd_vel_stop', self.velocity, 10, callback_group=group)
        self.server = ActionServer(
            self, NavigateToPose, 'navigate_to_pose', execute_callback=self.execute,
            goal_callback=self.accept, cancel_callback=lambda _: CancelResponse.ACCEPT,
            callback_group=group)

    def refine(self, request, response):
        del request
        self.events.append('refine')
        self.refinements += 1
        if self.refinements >= 3:
            self.degraded = False
        return response

    def clear(self, label, response):
        self.events.append('clear_'+label)
        return response

    def guard_ready(self, request, response):
        del request
        response.success = True
        return response

    def accept(self, request):
        """Optionally delay acceptance beyond the mission deadline."""
        del request
        if self.delay:
            # Release only after the mission expires, rather than racing wall-clock
            # sleep against the bounded cancellation timeout on a busy test host.
            if not self.accept_release.wait(timeout=10):
                return GoalResponse.REJECT
        return GoalResponse.ACCEPT

    def velocity(self, msg):
        """Count stop messages and fail if a test generates any drive command."""
        assert msg.linear.x == 0 and msg.angular.z == 0
        self.zeros += 1

    def publish_pose(self):
        """Publish current fake pose and stationary odometry."""
        transform = TransformStamped()
        transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id, transform.child_frame_id = 'map', 'base_link'
        transform.transform.translation.x, transform.transform.translation.y = self.position[:2]
        transform.transform.rotation.z, transform.transform.rotation.w = self.position[2:]
        self.tf.sendTransform(transform)
        odom = Odometry()
        odom.header.stamp = transform.header.stamp
        odom.header.frame_id, odom.child_frame_id = 'odom', 'base_link'
        odom.pose.pose.orientation.w = 1.
        self.odom.publish(odom)
        pose = PoseWithCovarianceStamped()
        pose.header.frame_id, pose.header.stamp = 'map', transform.header.stamp
        pose.pose.pose.position.x, pose.pose.pose.position.y = self.position[:2]
        pose.pose.pose.orientation = transform.transform.rotation
        pose.pose.covariance[0] = pose.pose.covariance[7] = .25 if self.degraded else .0004
        pose.pose.covariance[35] = .001
        self.amcl.publish(pose)
        scan = LaserScan()
        scan.header.frame_id = 'base_link'
        scan.header.stamp = (self.get_clock().now()-rclpy.duration.Duration(seconds=.08)).to_msg()
        scan.angle_min, scan.angle_increment = -math.pi, 2*math.pi/80
        scan.range_min, scan.range_max = .1, 20.
        yaw = 2*math.atan2(self.position[2], self.position[3])
        distances = []
        for i in range(80):
            angle = yaw+scan.angle_min+i*scan.angle_increment
            candidates = []
            for origin, direction in zip(self.position[:2], (math.cos(angle), math.sin(angle))):
                if abs(direction) > 1e-8:
                    candidates.append(((4.95 if direction>0 else -4.95)-origin)/direction)
            distances.append(min(candidates))
        scan.ranges = distances
        self.scan.publish(scan)

    def execute(self, handle):
        """Finish at the target, or await a real action cancellation."""
        pose = handle.request.pose.pose
        self.visits.append(time.monotonic())
        self.events.append('navigate')
        if self.fail_first and len(self.visits) == 1:
            self.degraded = True
            self.refinements = 0
            # Deliver poor quality before returning the failed action result.
            time.sleep(.1)
            handle.abort()
            result = NavigateToPose.Result()
            result.error_code = 208
            return result
        self.position = [pose.position.x, pose.position.y, pose.orientation.z, pose.orientation.w]
        if self.block:
            while not handle.is_cancel_requested:
                time.sleep(.01)
            self.cancellations += 1
            handle.canceled()
        else:
            handle.succeed()
        return NavigateToPose.Result()


@pytest.mark.parametrize('mode', ['success', 'recover', 'dwell_timeout', 'action_timeout', 'late_accept'])
def test_real_action_lifecycle_and_stop(tmp_path, monkeypatch, mode):
    """Exercise actual futures, TF/odom delivery, total timeout and cancellation."""
    assert os.environ.get('ROS_DOMAIN_ID') == '217'
    assert os.environ.get('ROS_AUTOMATIC_DISCOVERY_RANGE') == 'LOCALHOST'
    timeout = 30.0 if mode in ('success', 'recover') else 1.3
    package = Path(__file__).parents[1]
    monkeypatch.setattr(runtime, 'get_package_share_directory', lambda _: str(package))
    rclpy.init(args=[
        '--ros-args', '-p', 'goals:="BABA"', '-p', 'start_automatically:=true',
        '-p', f'mission_timeout_sec:={timeout}',
        # This suite checks action sequencing/deadlines, not host scheduler jitter.
        # Strict production freshness is covered by guard tests and real AMCL replay.
        '-p', 'telemetry_timeout_sec:=5.0', '-p', 'tf_timeout_sec:=5.0',
        '-p', 'localization_pose_timeout_sec:=5.0',
        '-p', f'result_file:={tmp_path / "result.json"}',
    ])
    fake = FakeNavigation(block=mode in ('action_timeout', 'late_accept'),
                          delay=2.0 if mode == 'late_accept' else 0, fail_first=mode == 'recover')
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(fake)
    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()
    node = runtime.MissionManager()
    node.waitUntilNav2Active = lambda: None
    monkeypatch.setattr(runtime.sys, 'stdin', type('Input', (), {'isatty': lambda _: False})())
    try:
        if mode in ('success', 'recover'):
            assert node.run_mission()
            assert len(fake.visits) == (5 if mode == 'recover' else 4)
            completed = fake.visits[1:] if mode == 'recover' else fake.visits
            assert all(b - a >= 3 for a, b in zip(completed, completed[1:]))
            assert time.monotonic() - fake.visits[-1] >= 3
            first_goal = fake.events.index('navigate')
            assert 'clear_global' in fake.events[:first_goal]
            assert 'clear_local' in fake.events[:first_goal]
            if mode == 'recover':
                start = fake.events.index('navigate')
                end = fake.events.index('navigate', start+1)
                recovery = fake.events[start+1:end]
                assert recovery.count('refine') >= 3
                assert recovery[-2:] == ['clear_global', 'clear_local']
        else:
            with pytest.raises(runtime.MissionExpired):
                node.run_mission()
        if mode == 'late_accept':
            fake.accept_release.set()
        confirmed = node.stop_task()
        if mode == 'late_accept' and not confirmed:
            # A bounded stop may correctly report unconfirmed when local DDS
            # delivery is delayed. Keep zeroing while the test peer completes
            # its handshake; no additional navigation goal may be sent.
            assert node._cancel_requested
            assert len(fake.visits) <= 1
            until = time.monotonic()+10.
            while not confirmed and time.monotonic() < until:
                confirmed = node.stop_task()
        assert confirmed
        assert fake.zeros > 0
        if mode in ('action_timeout', 'late_accept'):
            assert fake.cancellations == 1
    finally:
        fake.accept_release.set()
        node.stop_task()
        node.destroy_node()
        executor.shutdown(timeout_sec=3)
        thread.join(timeout=3)
        fake.destroy_node()
        rclpy.shutdown()
