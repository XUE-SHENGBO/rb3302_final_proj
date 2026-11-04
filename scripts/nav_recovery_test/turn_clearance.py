"""Exercise native NavFn with recorded lethal grids, without a robot or motion actions.

Run in localhost domain 217. Inputs are a baseline YAML and one or more rosbag
SQLite files containing /map, /global_costmap/costmap_raw, /tf and /tf_static.
The candidate is the repository navigation YAML. Outputs include plans, footprint
sweep checks and a comparison figure. Published maps have no external side effects.
"""
import argparse
import bisect
import json
import math
import os
from pathlib import Path
import signal
import sqlite3
import subprocess
import time

import numpy as np
import rclpy
from rclpy.action import ActionClient
from rclpy.duration import Duration
from rclpy.qos import DurabilityPolicy, QoSProfile
from rclpy.serialization import deserialize_message
from rclpy.time import Time
from rosidl_runtime_py.utilities import get_message
from geometry_msgs.msg import TransformStamped
from lifecycle_msgs.msg import Transition
from lifecycle_msgs.srv import ChangeState
from nav2_msgs.action import ComputePathToPose
from nav_msgs.msg import OccupancyGrid
from tf2_ros import Buffer
from tf2_ros.static_transform_broadcaster import StaticTransformBroadcaster
import yaml


def result(node, future, seconds=15):
    deadline = time.monotonic() + seconds
    while not future.done() and time.monotonic() < deadline:
        rclpy.spin_once(node, timeout_sec=.05)
    if not future.done():
        raise TimeoutError('native planner response timed out')
    return future.result()


def read_case(path, event):
    with sqlite3.connect(f'file:{path}?mode=ro', uri=True) as conn:
        def rows(topic):
            return [(t/1e9, deserialize_message(b, get_message(ty))) for t, b, ty in conn.execute(
                'select timestamp,data,t.type from messages m join topics t on m.topic_id=t.id '
                'where t.name=? order by timestamp', (topic,))]
        def before(topic):
            a = rows(topic)
            return a[bisect.bisect_right([t for t, _ in a], event)-1][1]
        scan = before('/scan')
        buffer = Buffer(cache_time=Duration(seconds=2000.))
        for topic in ('/tf_static', '/tf'):
            for _, msg in rows(topic):
                for tf in msg.transforms:
                    if topic == '/tf_static':
                        buffer.set_transform_static(tf, 'recording')
                    else:
                        buffer.set_transform(tf, 'recording')
        tf = buffer.lookup_transform('map', 'base_link', Time.from_msg(scan.header.stamp)).transform
        q = tf.rotation
        start = [tf.translation.x, tf.translation.y,
                 math.atan2(2*(q.w*q.z+q.x*q.y), 1-2*(q.y*q.y+q.z*q.z))]
        grid = before('/global_costmap/costmap_raw')
        m = grid.metadata
        occupancy = OccupancyGrid()
        occupancy.header.frame_id = 'map'
        occupancy.info.resolution = m.resolution
        occupancy.info.width, occupancy.info.height = m.size_x, m.size_y
        occupancy.info.origin = m.origin
        # Rebuild inflation with native plugins; retain recorded lethal/unknown cells.
        occupancy.data = [100 if v == 254 else -1 if v == 255 else 0 for v in grid.data]
        return occupancy, start


def bresenham(a, b):
    x, y = a
    u, v = b
    dx, dy = abs(u-x), abs(v-y)
    sx, sy = (1 if x < u else -1), (1 if y < v else -1)
    err = dx-dy
    while True:
        yield x, y
        if x == u and y == v:
            break
        e = 2*err
        if e > -dy:
            err -= dy
            x += sx
        if e < dx:
            err += dx
            y += sy


def sweep(plan, occupancy, footprint, padding):
    info = occupancy.info
    grid = np.array(occupancy.data).reshape(info.height, info.width)
    origin = np.array([info.origin.position.x, info.origin.position.y])
    vertices = np.array(footprint)
    vertices += np.sign(vertices)*padding
    unsafe = []
    # Sample every 1cm and each 5 degrees, including rotation in place at path bends.
    points = [plan[0]]
    for a, b in zip(plan, plan[1:]):
        for weight in np.linspace(0, 1, max(2, math.ceil(np.linalg.norm(b-a)/.01)+1))[1:]:
            points.append(a+(b-a)*weight)
    for p in points:
        collision = False
        for theta in np.arange(0, 2*math.pi, math.pi/36):
            c, s = math.cos(theta), math.sin(theta)
            poly = vertices @ np.array([[c, s], [-s, c]]) + p
            cells = np.floor((poly-origin)/info.resolution).astype(int)
            for a, b in zip(cells, np.roll(cells, -1, axis=0)):
                for x, y in bresenham(a, b):
                    if not (0 <= x < info.width and 0 <= y < info.height) or grid[y, x] == 100:
                        collision = True
                        break
                if collision:
                    break
            if collision:
                break
        if collision:
            unsafe.append(p.tolist())
    return {'samples': len(points), 'unsafe_samples': len(unsafe), 'unsafe_points': unsafe}


def run(config, occupancy, start, goal, folder, landmarks):
    config = yaml.safe_load(yaml.safe_dump(config))
    params = config['global_costmap']['global_costmap']['ros__parameters']
    params['plugins'] = ['static_layer', 'inflation_layer']
    params['initial_transform_timeout'] = 10.
    filename = folder/'params.yaml'
    filename.write_text(yaml.safe_dump(config))
    log = (folder/'planner.log').open('w')
    proc = subprocess.Popen(['/opt/ros/jazzy/lib/nav2_planner/planner_server', '--ros-args',
                             '--params-file', str(filename)], stdout=log, stderr=log)
    node = rclpy.create_node('turn_clearance_'+folder.name.replace('-', '_'))
    publisher = node.create_publisher(OccupancyGrid, '/map', QoSProfile(
        depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL))
    broadcaster = StaticTransformBroadcaster(node)
    tf = TransformStamped()
    tf.header.frame_id, tf.child_frame_id = 'map', 'base_link'
    tf.transform.translation.x, tf.transform.translation.y = start[:2]
    tf.transform.rotation.z, tf.transform.rotation.w = math.sin(start[2]/2), math.cos(start[2]/2)
    broadcaster.sendTransform(tf)
    occupancy.header.stamp = node.get_clock().now().to_msg()
    publisher.publish(occupancy)
    client = ActionClient(node, ComputePathToPose, '/compute_path_to_pose')
    try:
        service = node.create_client(ChangeState, '/planner_server/change_state')
        assert service.wait_for_service(timeout_sec=15)
        for transition in (Transition.TRANSITION_CONFIGURE, Transition.TRANSITION_ACTIVATE):
            request = ChangeState.Request()
            request.transition.id = transition
            assert result(node, service.call_async(request)).success
        deadline = time.monotonic()+1.5
        while time.monotonic() < deadline:
            rclpy.spin_once(node, timeout_sec=.05)
        assert client.wait_for_server(timeout_sec=10)
        request = ComputePathToPose.Goal()
        request.planner_id = 'GridBased'
        request.use_start = True
        for pose, xy in ((request.start, start[:2]), (request.goal, goal)):
            pose.header.frame_id = 'map'
            pose.header.stamp = node.get_clock().now().to_msg()
            pose.pose.position.x, pose.pose.position.y = map(float, xy)
            pose.pose.orientation.w = 1.
        handle = result(node, client.send_goal_async(request))
        assert handle.accepted
        response = result(node, handle.get_result_async())
        assert response.status == 4, str(response)
        path = np.array([[p.pose.position.x, p.pose.position.y] for p in response.result.path.poses])
        assert len(path) > 1
        reachability = {}
        for letter, xy in landmarks.items():
            request.goal.pose.position.x, request.goal.pose.position.y = map(float, xy[:2])
            request.goal.header.stamp = node.get_clock().now().to_msg()
            handle = result(node, client.send_goal_async(request))
            assert handle.accepted
            response = result(node, handle.get_result_async())
            reachability[letter] = {'status': response.status, 'error_code': response.result.error_code}
        return path, reachability
    finally:
        client.destroy()
        node.destroy_node()
        proc.send_signal(signal.SIGINT)
        try:
            proc.wait(timeout=8)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait()
        log.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--candidate', type=Path, required=True)
    parser.add_argument('--case', nargs=2, action='append', metavar=('BAG', 'START_UNIX'), required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--landmarks', type=Path, help='Also check no previously reachable letter becomes blocked')
    args = parser.parse_args()
    assert os.environ.get('ROS_DOMAIN_ID') == '217'
    assert os.environ.get('ROS_AUTOMATIC_DISCOVERY_RANGE') == 'LOCALHOST'
    args.output.mkdir(parents=True, exist_ok=True)
    baseline, candidate = [yaml.safe_load(p.read_text()) for p in (args.baseline, args.candidate)]
    landmarks = yaml.safe_load(args.landmarks.read_text())['letters'] if args.landmarks else {}
    local = candidate['local_costmap']['local_costmap']['ros__parameters']
    footprint = json.loads(local['footprint'])
    global_params = candidate['global_costmap']['global_costmap']['ros__parameters']
    inscribed = min(.11, .105)+global_params['footprint_padding']
    circumscribed = max(math.hypot(x+math.copysign(local['footprint_padding'], x),
                                  y+math.copysign(local['footprint_padding'], y)) for x, y in footprint)
    assert inscribed > circumscribed, (inscribed, circumscribed)
    rclpy.init()
    summary = {'global_inscribed_radius': inscribed, 'local_circumscribed_radius': circumscribed, 'cases': []}
    try:
        for n, (bag, event) in enumerate(args.case, 1):
            occupancy, start = read_case(Path(bag), float(event))
            record = {'bag': bag, 'event': float(event), 'start': start}
            for name, config in [('baseline', baseline), ('candidate', candidate)]:
                folder = args.output/f'case{n}-{name}'
                folder.mkdir(exist_ok=True)
                path, reachable = run(config, occupancy, start, [-.709623754, .485539317], folder, landmarks)
                check = sweep(path, occupancy, footprint, local['footprint_padding'])
                record[name] = {'plan': path.tolist(), 'landmarks': reachable, **check}
                print(f'case{n} {name}: path={len(path)}, unsafe sweep samples={check["unsafe_samples"]}', flush=True)
            summary['cases'].append(record)
            (args.output/'summary.json').write_text(json.dumps(summary, indent=2))
            assert record['candidate']['unsafe_samples'] == 0, f'case{n}: candidate rotation sweep touches lethal grid'
            lost = [letter for letter in landmarks
                    if record['baseline']['landmarks'][letter]['status'] == 4
                    and record['candidate']['landmarks'][letter]['status'] != 4]
            assert not lost, f'case{n}: previously reachable letters blocked: {lost}'
        (args.output/'summary.json').write_text(json.dumps(summary, indent=2))
        print('PASS native NavFn recorded-grid planning and rectangular rotation sweep', flush=True)
    finally:
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
