#!/usr/bin/env python3
"""Passive navigation evidence recorder; never sends goals, services or velocities."""
import json
import math
from pathlib import Path
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, QoSProfile, ReliabilityPolicy
from rclpy.serialization import deserialize_message
from rosidl_runtime_py.utilities import get_message
import rosbag2_py

TOPICS = {
    '/scan', '/tf', '/tf_static', '/odom', '/odom/raw', '/amcl_pose',
    '/initialpose', '/parameter_events', '/rosout', '/map', '/plan',
    '/local_plan', '/received_global_plan', '/is_rotating_to_heading',
    '/lookahead_point', '/lookahead_collision_arc',
    '/local_costmap/costmap', '/local_costmap/costmap_raw',
    '/local_costmap/costmap_updates', '/local_costmap/published_footprint',
    '/global_costmap/costmap', '/global_costmap/costmap_raw',
    '/global_costmap/costmap_updates', '/global_costmap/published_footprint',
    '/cmd_vel_nav_raw', '/cmd_vel_smoothed', '/cmd_vel', '/cmd_vel_stop',
    '/diagnostics', '/navigate_to_pose/_action/feedback',
    '/navigate_to_pose/_action/status', '/follow_path/_action/feedback',
    '/follow_path/_action/status',
}


class FailureProbe(Node):
    def __init__(self, directory):
        super().__init__('nav_failure_probe')
        self.directory = directory
        self.summary = (directory / 'snapshots.jsonl').open('w', buffering=1)
        self.writer = rosbag2_py.SequentialWriter()
        self.writer.open(
            rosbag2_py.StorageOptions(uri=str(directory / 'bag'), storage_id='sqlite3'),
            rosbag2_py.ConverterOptions('', ''))
        self.subscriptions_by_topic = {}
        self.latest = {}
        self.error_at = -math.inf
        self.create_timer(1.0, self.discover)
        self.create_timer(1.0, lambda: self.snapshot('periodic'))
        self.get_logger().info(f'Passive navigation recording: {directory}')

    def discover(self):
        for topic, types in self.get_topic_names_and_types():
            if topic not in TOPICS or topic in self.subscriptions_by_topic or not types:
                continue
            type_name = types[0]
            cls = get_message(type_name)
            self.writer.create_topic(rosbag2_py.TopicMetadata(
                id=len(self.subscriptions_by_topic) + 1, name=topic, type=type_name, serialization_format='cdr'))
            qos = QoSProfile(depth=50, reliability=ReliabilityPolicy.BEST_EFFORT)
            if topic in ('/tf_static', '/map'):
                qos.durability = DurabilityPolicy.TRANSIENT_LOCAL
                qos.reliability = ReliabilityPolicy.RELIABLE
            callback = lambda raw, t=topic, c=cls: self.receive(t, c, raw)
            self.subscriptions_by_topic[topic] = self.create_subscription(
                cls, topic, callback, qos, raw=True)
            self.get_logger().info(f'Recording {topic}: {type_name}')

    def receive(self, topic, cls, raw):
        now = self.get_clock().now().nanoseconds
        self.writer.write(topic, raw, now)
        # Full scans, costmaps, footprints and TF stay in the bag for replay.
        if topic in ('/amcl_pose', '/odom', '/lookahead_collision_arc', '/scan', '/is_rotating_to_heading') or topic.startswith('/cmd_vel'):
            self.latest[topic] = (time.monotonic(), deserialize_message(raw, cls))
        if topic == '/rosout':
            msg = deserialize_message(raw, cls)
            if msg.level >= 40 and time.monotonic() - self.error_at > .2:
                self.error_at = time.monotonic()
                self.snapshot(f'{msg.name}: {msg.msg}')

    def snapshot(self, trigger):
        record = {'unix_ns': self.get_clock().now().nanoseconds, 'trigger': trigger,
                  'recording_topics': sorted(self.subscriptions_by_topic), 'state': {}}
        for topic, (received, msg) in self.latest.items():
            item = {'receive_age_sec': round(time.monotonic() - received, 3)}
            if topic.startswith('/cmd_vel'):
                item.update(v=msg.linear.x, w=msg.angular.z)
            elif topic == '/scan':
                finite = [r for r in msg.ranges if math.isfinite(r)]
                item.update(frame=msg.header.frame_id, beams=len(msg.ranges),
                            finite=len(finite), positive_inf=sum(r == math.inf for r in msg.ranges),
                            nan=sum(math.isnan(r) for r in msg.ranges),
                            minimum_finite=min(finite) if finite else None)
            elif topic == '/is_rotating_to_heading':
                item['value'] = msg.data
            elif topic == '/lookahead_collision_arc':
                item.update(frame=msg.header.frame_id, count=len(msg.poses),
                            xy=[[p.pose.position.x, p.pose.position.y] for p in msg.poses])
            else:
                p = msg.pose.pose
                q = p.orientation
                item.update(x=p.position.x, y=p.position.y,
                            yaw=math.atan2(2*(q.w*q.z+q.x*q.y), 1-2*(q.y*q.y+q.z*q.z)))
                if topic == '/odom':
                    item.update(v=msg.twist.twist.linear.x, w=msg.twist.twist.angular.z)
            record['state'][topic] = item
        self.summary.write(json.dumps(record, ensure_ascii=False) + '\n')
        if trigger != 'periodic' and rclpy.ok():
            self.get_logger().info('Failure snapshot: ' + json.dumps(record, ensure_ascii=False))


def main():
    directory = Path.home() / '.ros/rb3302/nav_diagnostics' / time.strftime('%Y%m%d-%H%M%S')
    directory.mkdir(parents=True, exist_ok=False)
    rclpy.init()
    node = FailureProbe(directory)
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        pass
    finally:
        node.snapshot('recorder_shutdown')
        node.writer.close()
        node.summary.close()
        node.destroy_node()
        rclpy.try_shutdown()


if __name__ == '__main__':
    main()
