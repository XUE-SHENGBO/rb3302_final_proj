"""Execute ordered map-frame goals using the configured Nav2 A* + RPP stack.

Start planning_rpp/planning.launch.py separately. Coordinates are deliberately
not supplied by default: the project brief does not specify a route.
"""

import math
import time

import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.parameter import Parameter
from rclpy.signals import SignalHandlerOptions


def parse_poses(values, name, single=False):
    """Validate a flattened ROS double array of x, y, yaw triples."""
    if not values or len(values) % 3 or (single and len(values) != 3):
        raise ValueError(f'{name} must contain ' + (
            'exactly [x, y, yaw]' if single else '[x1, y1, yaw1, x2, y2, yaw2, ...]'))
    if not all(math.isfinite(value) for value in values):
        raise ValueError(f'{name} must contain only finite numbers')
    return [tuple(values[index:index + 3]) for index in range(0, len(values), 3)]


class MissionManager(BasicNavigator):
    """Send one goal at a time; never skip a failed or timed-out goal."""

    def __init__(self):
        super().__init__(node_name='mission_manager')
        self.declare_parameter('goals', Parameter.Type.DOUBLE_ARRAY)
        self.declare_parameter('initial_pose', Parameter.Type.DOUBLE_ARRAY)
        self.declare_parameter('set_initial_pose', False)
        self.declare_parameter('map_frame', 'map')
        self.declare_parameter('goal_timeout_sec', 180.0)
        self._task_active = False

    def make_pose(self, coordinates):
        """Create a stamped map pose with a normalized yaw quaternion."""
        x, y, yaw = coordinates
        pose = PoseStamped()
        pose.header.frame_id = self.get_parameter('map_frame').value
        pose.header.stamp = self.get_clock().now().to_msg()
        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.orientation.z = math.sin(yaw / 2.0)
        pose.pose.orientation.w = math.cos(yaw / 2.0)
        return pose

    def stop_task(self):
        """Request cancellation of the active Nav2 goal."""
        if self._task_active:
            self.cancelTask()
            self._task_active = False

    def run_mission(self):
        """Wait for localisation, then navigate the configured route in order."""
        # Validate the complete mission before submitting any motion request.
        goals = parse_poses(self.get_parameter('goals').value, 'goals')
        timeout = self.get_parameter('goal_timeout_sec').value
        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError('goal_timeout_sec must be finite and positive')
        if not self.get_parameter('map_frame').value.strip():
            raise ValueError('map_frame must not be empty')
        if self.get_parameter('set_initial_pose').value:
            initial = parse_poses(
                self.get_parameter('initial_pose').value, 'initial_pose', single=True)[0]
            self.setInitialPose(self.make_pose(initial))

        self.get_logger().info(
            'Waiting for Nav2 and AMCL. Set the actual initial pose in RViz '
            'unless it was supplied through parameters.')
        self.waitUntilNav2Active()

        for index, coordinates in enumerate(goals, start=1):
            self.get_logger().info(f'Goal {index}/{len(goals)}: {coordinates}')
            started = time.monotonic()
            # The default navigation BT runs GridBased (A*) and FollowPath (RPP),
            # including replanning and recovery, as configured in planning_rpp.
            if not self.goToPose(self.make_pose(coordinates)):
                self.get_logger().error(f'Goal {index} was rejected; mission stopped')
                return False
            self._task_active = True
            while not self.isTaskComplete():
                if time.monotonic() - started >= timeout:
                    self.get_logger().error(f'Goal {index} timed out; cancelling mission')
                    self.stop_task()
                    return False
                # isTaskComplete spins the navigator to process action feedback.
            self._task_active = False
            result = self.getResult()
            if result != TaskResult.SUCCEEDED:
                self.get_logger().error(
                    f'Goal {index} did not succeed ({result}); mission stopped')
                return False
            self.get_logger().info(f'Goal {index} reached')

        self.get_logger().info('All goals reached in order')
        return True


def main(args=None):
    """Run the configured mission and return a nonzero exit code on failure."""
    rclpy.init(args=args, signal_handler_options=SignalHandlerOptions.NO)
    navigator = None
    exit_code = 1
    try:
        navigator = MissionManager()
        exit_code = 0 if navigator.run_mission() else 1
    except KeyboardInterrupt:
        exit_code = 130
    except Exception as error:
        if navigator is not None:
            navigator.get_logger().error(f'Mission stopped: {error}')
        else:
            print(f'Mission setup failed: {error}')
    finally:
        if navigator is not None:
            try:
                if rclpy.ok():
                    navigator.stop_task()
            finally:
                navigator.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
