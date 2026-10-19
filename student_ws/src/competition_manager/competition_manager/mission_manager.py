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

letter_pos_map={
    'A':(1.6514630317687988,-0.08509742468595505),
    'B':(1.088031530380249, -0.10565447062253952),
    'C':(0.46405327320098877,-0.09198123961687088),
    'D':(-0.11078454554080963,-0.08715619891881943),
    'E':(-0.6893330812454224,-0.10935278981924057),
    'F':(-1.2777215242385864,-0.085807204246521),
    'G':(1.6867185831069946,0.4627726376056671),
    'H':(1.0710629224777222,0.46948617696762085),
    'I':(0.5010952353477478,0.4675194323062897),
    'J':(-0.09818114340305328,0.4497152864933014),
    'K':(-0.7096237540245056,0.4855393171310425),
    'L':(-1.2867027521133423,0.47032997012138367),
    'M':(1.663408875465393,1.0750311613082886),
    'N':(1.1118243932724,1.0824636220932007),
    'O':(0.46875935792922974,1.0902024507522583),
    'P':(-0.09403415769338608,1.0922552347183228),
    'Q':(-0.6912289261817932,1.0864468812942505),
    'R':(-1.2855602502822876,1.1045721769332886),
    'S':(1.6706331968307495,1.6458920240402222),
    'T':(1.102006196975708,1.6640079021453857),
    'U':(0.49858278036117554,1.6451228857040405),
    'V':(-0.10852397978305817,1.670001745223999),
    'W':(-0.7471744418144226,1.6658536195755005),
    'X':(-1.275559425354004,1.6493488550186157),
}

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
        self.declare_parameter('goals', Parameter.Type.STRING)
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
        goals_str = self.get_parameter('goals').value
        if not isinstance(goals_str, str):
            raise ValueError('goals must be a letter route such as "ABC" or "A,B,C"')
        letters = ''.join(goals_str.upper().replace(',', ' ').split())
        if not letters:
            raise ValueError('goals must contain at least one letter from A to X')
        unknown = sorted(set(letters) - letter_pos_map.keys())
        if unknown:
            raise ValueError(f'goals contains unknown letters: {", ".join(unknown)}')
        # The measured map contains positions only; use map-frame yaw 0 radians.
        goals = [(*letter_pos_map[letter], 0.0) for letter in letters]
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
