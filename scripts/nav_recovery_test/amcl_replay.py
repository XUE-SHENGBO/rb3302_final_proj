"""Freeze stationary sensor frames from a real bag and refine actual AMCL.

No navigation/controller servers are started. Localhost domain 217 is mandatory.
"""
import argparse
import copy
import json
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
from lifecycle_msgs.msg import Transition
from lifecycle_msgs.srv import ChangeState
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import OccupancyGrid, Odometry
from sensor_msgs.msg import LaserScan
from tf2_ros import StaticTransformBroadcaster
import yaml

assert os.environ.get('ROS_DOMAIN_ID') == '217'
assert os.environ.get('ROS_AUTOMATIC_DISCOVERY_RANGE') == 'LOCALHOST'
parser = argparse.ArgumentParser()
parser.add_argument('bag', type=Path)
parser.add_argument('--output', type=Path, required=True)
parser.add_argument('--hold-ready-seconds', type=float, default=0.)
args = parser.parse_args()
root = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(root/'student_ws/src/competition_manager'))
from competition_manager import mission_manager as runtime
runtime.get_package_share_directory = lambda _: str(root/'student_ws/src/competition_manager')
connection = sqlite3.connect(f'file:{args.bag.resolve()}?mode=ro', uri=True)


def messages(name):
    return [(t/1e9, deserialize_message(raw, get_message(ty)))
            for t, raw, ty in connection.execute(
                'select timestamp,data,t.type from messages m join topics t on m.topic_id=t.id '
                'where t.name=? order by timestamp', (name,))]


static_map = messages('/map')[0][1]
initial = messages('/initialpose')[0][1]
scans = [m for t,m in messages('/scan') if 1793779299 <= t <= 1793779301.7]
assert scans, 'expected stationary frames preceding KNHX'
static_transforms = messages('/tf_static')[0][1].transforms
odom_tf = next(tf for t,m in reversed(messages('/tf')) if t <= 1793779301.7
               for tf in m.transforms if tf.header.frame_id == 'odom' and tf.child_frame_id == 'base_link')
work = Path(tempfile.mkdtemp(prefix='amcl-stationary-replay-'))
params = yaml.safe_load((root/'student_ws/src/planning_rpp/config/nav2_params.yaml').read_text())
(work/'amcl.yaml').write_text(yaml.safe_dump({'amcl': params['amcl']}))
log = (work/'amcl.log').open('w')
proc = subprocess.Popen(['/opt/ros/jazzy/lib/nav2_amcl/amcl', '--ros-args', '--params-file',
                         str(work/'amcl.yaml')], stdout=log, stderr=subprocess.STDOUT)
rclpy.init()
fake = Node('recorded_stationary_sensors')
map_pub = fake.create_publisher(OccupancyGrid, '/map', QoSProfile(
    depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL))
scan_pub = fake.create_publisher(LaserScan, '/scan', 10)
odom_pub = fake.create_publisher(Odometry, '/odom', 10)
initial_pub = fake.create_publisher(PoseWithCovarianceStamped, '/initialpose', 10)
broadcaster = StaticTransformBroadcaster(fake)
broadcaster.sendTransform(static_transforms+[odom_tf])
map_pub.publish(static_map)
index = 0


def publish():
    global index
    scan = copy.deepcopy(scans[index % len(scans)])
    index += 1
    scan.header.stamp = (fake.get_clock().now()-rclpy.duration.Duration(seconds=.12)).to_msg()
    scan_pub.publish(scan)
    odom = Odometry()
    odom.header.stamp = fake.get_clock().now().to_msg()
    odom.header.frame_id, odom.child_frame_id = 'odom', 'base_link'
    odom.pose.pose.orientation.w = 1.
    odom_pub.publish(odom)


fake.create_timer(.13, publish)
executor = MultiThreadedExecutor(num_threads=2)
executor.add_node(fake)
thread = threading.Thread(target=executor.spin, daemon=True)
thread.start()
node = runtime.MissionManager()


def call_change(transition):
    client = node.create_client(ChangeState, '/amcl/change_state')
    try:
        assert client.wait_for_service(timeout_sec=10)
        request = ChangeState.Request()
        request.transition.id = transition
        future = client.call_async(request)
        end = time.monotonic()+10
        while not future.done() and time.monotonic() < end:
            node._spin()
        assert future.done() and future.result().success
    finally:
        node.destroy_client(client)


try:
    call_change(Transition.TRANSITION_CONFIGURE)
    call_change(Transition.TRANSITION_ACTIVATE)
    initial.header.stamp = node.get_clock().now().to_msg()
    initial_pub.publish(initial)
    end = time.monotonic()+3
    while time.monotonic() < end:
        node._spin()
    before = node._loc_pose[1] if node._loc_pose else None
    refined = node.ensure_localization(force=True)
    waited = None
    if args.hold_ready_seconds > 0:
        # Exercise actual production READY handling with a stationary AMCL that
        # publishes only when explicitly updated. No navigation goal is sent.
        node._state = {'started_at_unix': None, 'status': 'preparing', 'visits': []}
        node._result_path = str(work/'ready-test-checkpoint.json')
        start = time.monotonic()
        trigger = threading.Timer(args.hold_ready_seconds, node._start_requested.set)
        trigger.start()
        try:
            node._wait_for_start()
        finally:
            trigger.cancel()
            trigger.join(timeout=1)
        waited = time.monotonic()-start
        assert waited >= args.hold_ready_seconds and node._deadline is not None
    after = node._loc_pose[1]
    report = {'refined': refined, 'quality': node._localization_quality(), 'logs': str(work),
              'ready_wait_seconds': waited,
              'before_covariance': [before.pose.covariance[i] for i in (0,7,35)] if before else None,
              'after_covariance': [after.pose.covariance[i] for i in (0,7,35)],
              'after_pose': [after.pose.pose.position.x, after.pose.pose.position.y]}
    args.output.write_text(json.dumps(report, indent=2))
    print(json.dumps(report, indent=2))
    assert refined and report['quality'][0]
finally:
    executor.shutdown(timeout_sec=3)
    thread.join(timeout=3)
    fake.destroy_node()
    node.destroy_node()
    rclpy.try_shutdown()
    proc.send_signal(signal.SIGINT)
    try:
        proc.wait(timeout=8)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
    log.close()
