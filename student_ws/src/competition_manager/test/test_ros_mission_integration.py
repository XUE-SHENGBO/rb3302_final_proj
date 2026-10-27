"""Opt-in ROS action integration on an isolated domain, never physical hardware."""

import os
from pathlib import Path
import sys
import threading
import time

import pytest

sys.path.insert(0, str(Path(__file__).parents[1]))
from competition_manager import mission_manager as runtime  # noqa: E402, I100
from geometry_msgs.msg import TransformStamped, Twist  # noqa: E402
from nav2_msgs.action import NavigateToPose  # noqa: E402
from nav_msgs.msg import Odometry  # noqa: E402
import rclpy  # noqa: E402
from rclpy.action import ActionServer, CancelResponse, GoalResponse  # noqa: E402
from rclpy.callback_groups import ReentrantCallbackGroup  # noqa: E402
from rclpy.executors import MultiThreadedExecutor  # noqa: E402
from rclpy.node import Node  # noqa: E402
from tf2_ros import TransformBroadcaster  # noqa: E402


pytestmark = pytest.mark.skipif(
    os.environ.get('RB3302_ROS_INTEGRATION') != '1', reason='Isolated ROS integration is opt-in')


class FakeNavigation(Node):
    """Publish synthetic pose/odometry and implement only the navigation action."""

    def __init__(self, block=False, delay=0):
        super().__init__('fake_navigation')
        self.position = [0., 0., 0., 1.]
        self.block, self.delay = block, delay
        self.visits = []
        self.cancellations = 0
        self.zeros = 0
        group = ReentrantCallbackGroup()
        self.tf = TransformBroadcaster(self)
        self.odom = self.create_publisher(Odometry, '/odom', 10)
        self.create_timer(.02, self.publish_pose, callback_group=group)
        self.create_subscription(Twist, '/cmd_vel', self.velocity, 10, callback_group=group)
        self.server = ActionServer(
            self, NavigateToPose, 'navigate_to_pose', execute_callback=self.execute,
            goal_callback=self.accept, cancel_callback=lambda _: CancelResponse.ACCEPT,
            callback_group=group)

    def accept(self, request):
        """Optionally delay acceptance beyond the mission deadline."""
        del request
        time.sleep(self.delay)
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

    def execute(self, handle):
        """Finish at the target, or await a real action cancellation."""
        pose = handle.request.pose.pose
        self.visits.append(time.monotonic())
        self.position = [pose.position.x, pose.position.y, pose.orientation.z, pose.orientation.w]
        if self.block:
            while not handle.is_cancel_requested:
                time.sleep(.01)
            self.cancellations += 1
            handle.canceled()
        else:
            handle.succeed()
        return NavigateToPose.Result()


@pytest.mark.parametrize('mode', ['success', 'dwell_timeout', 'action_timeout', 'late_accept'])
def test_real_action_lifecycle_and_stop(tmp_path, monkeypatch, mode):
    """Exercise actual futures, TF/odom delivery, total timeout and cancellation."""
    assert os.environ.get('ROS_DOMAIN_ID') == '217'
    assert os.environ.get('ROS_AUTOMATIC_DISCOVERY_RANGE') == 'LOCALHOST'
    timeout = 30.0 if mode == 'success' else 1.3
    package = Path(__file__).parents[1]
    monkeypatch.setattr(runtime, 'get_package_share_directory', lambda _: str(package))
    rclpy.init(args=[
        '--ros-args', '-p', 'goals:="BABA"', '-p', 'start_automatically:=true',
        '-p', f'mission_timeout_sec:={timeout}',
        '-p', f'result_file:={tmp_path / "result.json"}',
    ])
    fake = FakeNavigation(block=mode in ('action_timeout', 'late_accept'),
                          delay=2.0 if mode == 'late_accept' else 0)
    executor = MultiThreadedExecutor(num_threads=4)
    executor.add_node(fake)
    thread = threading.Thread(target=executor.spin, daemon=True)
    thread.start()
    node = runtime.MissionManager()
    node.waitUntilNav2Active = lambda: None
    monkeypatch.setattr(runtime.sys, 'stdin', type('Input', (), {'isatty': lambda _: False})())
    try:
        if mode == 'success':
            assert node.run_mission()
            assert len(fake.visits) == 4
            assert all(b - a >= 3 for a, b in zip(fake.visits, fake.visits[1:]))
            assert time.monotonic() - fake.visits[-1] >= 3
        else:
            with pytest.raises(runtime.MissionExpired):
                node.run_mission()
        assert node.stop_task()
        assert fake.zeros > 0
        if mode in ('action_timeout', 'late_accept'):
            assert fake.cancellations == 1
    finally:
        node.stop_task()
        node.destroy_node()
        executor.shutdown(timeout_sec=3)
        thread.join(timeout=3)
        fake.destroy_node()
        rclpy.shutdown()
