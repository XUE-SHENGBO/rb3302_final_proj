"""Real Nav2 planner/costmap regression on localhost domain 217; synthetic scans only."""
import math
import os
from pathlib import Path
import signal
import subprocess
import tempfile
import time

import rclpy
from rclpy.action import ActionClient
from rclpy.qos import QoSProfile, DurabilityPolicy
from geometry_msgs.msg import TransformStamped
from lifecycle_msgs.msg import Transition
from lifecycle_msgs.srv import ChangeState
from nav2_msgs.action import ComputePathToPose
from nav2_msgs.srv import ClearEntireCostmap, GetCostmap
from nav_msgs.msg import OccupancyGrid
from sensor_msgs.msg import LaserScan
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster

assert os.environ.get('ROS_DOMAIN_ID') == '217'
assert os.environ.get('ROS_AUTOMATIC_DISCOVERY_RANGE') == 'LOCALHOST'
root = Path(__file__).resolve().parents[2]
work = Path(tempfile.mkdtemp(prefix='knhx-global-refresh-'))
log = (work / 'planner.log').open('w')
proc = subprocess.Popen([
    '/opt/ros/jazzy/lib/nav2_planner/planner_server', '--ros-args', '--params-file',
    str(root / 'student_ws/src/planning_rpp/config/nav2_params.yaml')],
    stdout=log, stderr=subprocess.STDOUT)
rclpy.init()
node = rclpy.create_node('synthetic_global_refresh_test')
map_pub = node.create_publisher(OccupancyGrid, '/map', QoSProfile(
    depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL))
scan_pub = node.create_publisher(LaserScan, '/scan', 10)
broadcaster = StaticTransformBroadcaster(node)
transforms = []
for parent, child in [('map', 'odom'), ('odom', 'base_link'), ('base_link', 'laser')]:
    tf = TransformStamped()
    tf.header.frame_id, tf.child_frame_id = parent, child
    tf.transform.rotation.w = 1.
    transforms.append(tf)
broadcaster.sendTransform(transforms)
static = OccupancyGrid()
static.header.frame_id = 'map'
static.info.resolution = .05
static.info.width = static.info.height = 60
static.info.origin.position.x = static.info.origin.position.y = -1.5
static.info.origin.orientation.w = 1.
static.data = [0] * 3600
for y in range(20, 41):
    static.data[y * 60 + 46] = 100  # Wall at x=.825, independent of scans.
map_pub.publish(static)
scan = LaserScan()
scan.header.frame_id = 'laser'
scan.angle_min, scan.angle_increment = -math.pi, math.pi / 180
scan.angle_max = math.pi - scan.angle_increment
scan.range_min, scan.range_max, scan.scan_time = .15, 12., .1
mode = 'old'


def publish():
    scan.header.stamp = node.get_clock().now().to_msg()
    scan.ranges = [math.inf] * 360
    if mode == 'old':
        scan.ranges[181] = .425
    elif mode == 'fresh':
        scan.ranges[181] = .325
    scan_pub.publish(scan)


node.create_timer(.05, publish)


def spin(seconds):
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        rclpy.spin_once(node, timeout_sec=.05)


def result(future):
    end = time.monotonic() + 12
    while not future.done() and time.monotonic() < end:
        rclpy.spin_once(node, timeout_sec=.05)
    assert future.done(), 'response timeout'
    return future.result()


def call(service, name, request):
    client = node.create_client(service, name)
    try:
        assert client.wait_for_service(timeout_sec=12), name
        return result(client.call_async(request))
    finally:
        node.destroy_client(client)


def cost(x, y):
    grid = call(GetCostmap, '/global_costmap/get_costmap', GetCostmap.Request()).map
    info = grid.metadata
    i = math.floor((x - info.origin.position.x) / info.resolution)
    j = math.floor((y - info.origin.position.y) / info.resolution)
    return grid.data[j * info.size_x + i]


planner = ActionClient(node, ComputePathToPose, '/compute_path_to_pose')


def plan():
    assert planner.wait_for_server(timeout_sec=5)
    goal = ComputePathToPose.Goal()
    goal.planner_id = 'GridBased'
    goal.goal.header.frame_id = 'map'
    goal.goal.pose.position.x, goal.goal.pose.position.y = .425, .025
    goal.goal.pose.orientation.w = 1.
    handle = result(planner.send_goal_async(goal))
    assert handle.accepted
    return result(handle.get_result_async())


def clear():
    call(ClearEntireCostmap, '/global_costmap/clear_entirely_global_costmap',
         ClearEntireCostmap.Request())
    spin(1.)


try:
    for transition in (Transition.TRANSITION_CONFIGURE, Transition.TRANSITION_ACTIVATE):
        request = ChangeState.Request()
        request.transition.id = transition
        assert call(ChangeState, '/planner_server/change_state', request).success
    spin(1.5)
    assert cost(.425, .025) == 254
    mode = 'empty'
    spin(1.)
    assert cost(.425, .025) == 254, 'expected retained mark with inf ignored'
    blocked = plan()
    assert blocked.status == 6 and blocked.result.error_code == 208, blocked
    clear()
    assert cost(.425, .025) < 253, 'old observation remained after refresh'
    assert cost(.825, .025) == 254, 'static wall lost'
    recovered = plan()
    assert recovered.status == 4 and recovered.result.path.poses, recovered
    mode = 'fresh'
    spin(1.)
    assert cost(.325, .025) == 254, 'new finite obstacle not marked'
    clear()
    assert cost(.325, .025) == 254, 'persistent visible obstacle lost after refresh'
    assert cost(.825, .025) == 254, 'static wall lost after second refresh'
    mode = 'old'
    spin(1.)
    clear()
    still_blocked = plan()
    assert still_blocked.status == 6 and still_blocked.result.error_code == 208
    print('PASS actual NavFn: stale mark -> 208; refresh -> valid path; '
          'static wall retained; fresh/persistent real observations still block; logs=' + str(work))
finally:
    planner.destroy()
    node.destroy_node()
    rclpy.try_shutdown()
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=8)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
    log.close()
