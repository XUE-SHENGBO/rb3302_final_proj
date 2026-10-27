#!/usr/bin/env python3
"""Local differential drive and laser simulation against the real occupancy map."""
import argparse
import json
import math
import os
import time
from pathlib import Path

import yaml
from PIL import Image
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from geometry_msgs.msg import TransformStamped, Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import Imu, LaserScan
from tf2_ros import Buffer, StaticTransformBroadcaster, TransformException, TransformListener
from rclpy.time import Time

ROOT = Path(__file__).resolve().parent


def quaternion(yaw):
    return (math.sin(yaw / 2.0), math.cos(yaw / 2.0))


def advance_motion(maze, pose, velocity, dt, length, width):
    """Consume the full elapsed interval with small collision-checked steps."""
    x, y, yaw = pose
    v, w = velocity
    if dt <= 0 or (v == 0 and w == 0):
        return pose, 0.0, False
    steps = max(1, math.ceil(dt / 0.01))
    h = dt / steps
    travelled = 0.0
    for _ in range(steps):
        mid = yaw + w * h / 2
        nx, ny, nyaw = x + v * h * math.cos(mid), y + v * h * math.sin(mid), yaw + w * h
        if maze.collides(nx, ny, nyaw, length, width):
            return (x, y, yaw), travelled, True
        x, y, yaw = nx, ny, nyaw
        travelled += v * h
    return (x, y, yaw), travelled, False


class Maze:
    def __init__(self, yaml_path):
        self.yaml_path = Path(yaml_path)
        info = yaml.safe_load(self.yaml_path.read_text())
        if info.get('negate', 0) or info['origin'][2] != 0:
            raise ValueError('Simulator requires a non-negated map with zero origin rotation')
        self.resolution = float(info['resolution'])
        self.origin = tuple(info['origin'][:2])
        self.image = Image.open(self.yaml_path.parent / info['image']).convert('L')
        self.width, self.height = self.image.size
        self.pixels = self.image.load()
        self.threshold = 255 * (1.0 - float(info.get('free_thresh', 0.196)))

    def blocked(self, x, y):
        col = math.floor((x - self.origin[0]) / self.resolution)
        row = self.height - 1 - math.floor((y - self.origin[1]) / self.resolution)
        return not (0 <= col < self.width and 0 <= row < self.height) or self.pixels[col, row] < self.threshold

    def point(self, x, y, scale):
        return ((x - self.origin[0]) / self.resolution * scale,
                (self.height - (y - self.origin[1]) / self.resolution) * scale)

    def collides(self, x, y, yaw, length, width):
        # Sample the full rectangular body at <= half a map cell, including edges.
        nx = math.ceil(length / (self.resolution / 2)); ny = math.ceil(width / (self.resolution / 2))
        c, s = math.cos(yaw), math.sin(yaw)
        for i in range(nx + 1):
            px = -length / 2 + length * i / nx
            for j in range(ny + 1):
                py = -width / 2 + width * j / ny
                if self.blocked(x + c * px - s * py, y + s * px + c * py):
                    return True
        return False

    def ray(self, x, y, angle, minimum, maximum):
        c, s = math.cos(angle), math.sin(angle)
        step = self.resolution / 3
        distance = 0.0
        while distance <= maximum:
            if self.blocked(x + distance * c, y + distance * s):
                return distance if distance >= minimum else float('inf')
            distance += step
        return float('inf')


class Simulator(Node):
    def __init__(self, cfg, maze):
        super().__init__('rb3302_simulator')
        self.cfg, self.maze = cfg, maze
        self.robot, self.scan_cfg = cfg['robot'], cfg['scan']
        pose = cfg['initial_pose']; self.x = float(pose['x']); self.y = float(pose['y']); self.yaw = float(pose['yaw'])
        self.initial = (self.x, self.y, self.yaw)
        if maze.collides(self.x, self.y, self.yaw, self.robot['length'], self.robot['width']):
            raise ValueError('Initial robot footprint overlaps a wall or unknown map space')
        self.v = self.w = 0.0; self.last_cmd = 0.0; self.last_tick = time.monotonic(); self.blocked = False
        self.scan_pub = self.create_publisher(LaserScan, '/scan', qos_profile_sensor_data)
        self.odom_pub = self.create_publisher(Odometry, '/odom/raw', 10)
        self.truth_pub = self.create_publisher(Odometry, '/sim/ground_truth', 10)
        self.imu_pub = self.create_publisher(Imu, '/imu_data_ros', qos_profile_sensor_data)
        self.create_subscription(Twist, '/cmd_vel', self.command, 10)
        self.static_tf = StaticTransformBroadcaster(self)
        transform = TransformStamped(); transform.header.stamp = self.get_clock().now().to_msg()
        transform.header.frame_id = 'base_link'; transform.child_frame_id = 'laser'
        transform.transform.translation.x = float(self.robot['laser_x']); transform.transform.translation.z = float(self.robot['laser_height'])
        transform.transform.rotation.z, transform.transform.rotation.w = quaternion(float(self.robot['laser_yaw']))
        self.static_tf.sendTransform(transform)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        trace_dir = Path(os.environ.get('ROS_LOG_DIR', str(ROOT / 'log')))
        trace_dir.mkdir(parents=True, exist_ok=True)
        self.trace = (trace_dir / f'sim_trace_{os.getpid()}.jsonl').open('w')
        self.actual_velocity = (0.0, 0.0)
        self.latest_scan = []
        self.create_timer(0.02, self.tick)
        self.create_timer(1.0 / float(self.scan_cfg['rate_hz']), self.scan)
        self.create_timer(0.5, self.audit)
        self.get_logger().info(f'Simulation pose: x={self.x:.3f}, y={self.y:.3f}, yaw={self.yaw:.3f}')

    def command(self, msg):
        self.v, self.w = float(msg.linear.x), float(msg.angular.z)
        self.last_cmd = time.monotonic()

    def tick(self):
        now = time.monotonic(); dt = now - self.last_tick; self.last_tick = now
        v, w = (self.v, self.w) if now - self.last_cmd < float(self.robot['command_timeout']) else (0.0, 0.0)
        old_yaw = self.yaw
        pose, distance, self.blocked = advance_motion(
            self.maze, (self.x, self.y, self.yaw), (v, w), dt,
            self.robot['length'], self.robot['width'])
        self.x, self.y, self.yaw = pose
        v = distance / dt if dt > 0 else 0.0
        w = (self.yaw - old_yaw) / dt if dt > 0 else 0.0
        self.actual_velocity = (v, w)
        stamp = self.get_clock().now().to_msg(); ix, iy, iyaw = self.initial
        dx, dy = self.x - ix, self.y - iy; c, s = math.cos(iyaw), math.sin(iyaw)
        relative_yaw = self.yaw - iyaw
        odom = Odometry(); odom.header.stamp = stamp; odom.header.frame_id = 'odom'; odom.child_frame_id = 'base_link'
        odom.pose.pose.position.x = c * dx + s * dy; odom.pose.pose.position.y = -s * dx + c * dy
        odom.pose.pose.orientation.z, odom.pose.pose.orientation.w = quaternion(relative_yaw)
        odom.twist.twist.linear.x = v; odom.twist.twist.angular.z = w
        odom.twist.covariance[0] = 0.001; odom.twist.covariance[35] = 0.001
        self.odom_pub.publish(odom)
        truth = Odometry(); truth.header.stamp = stamp; truth.header.frame_id = 'map'; truth.child_frame_id = 'base_link'
        truth.pose.pose.position.x = self.x; truth.pose.pose.position.y = self.y
        truth.pose.pose.orientation.z, truth.pose.pose.orientation.w = quaternion(self.yaw)
        truth.twist.twist.linear.x = v; truth.twist.twist.angular.z = w
        self.truth_pub.publish(truth)
        imu = Imu(); imu.header.stamp = stamp; imu.header.frame_id = 'base_link'
        imu.orientation.z, imu.orientation.w = quaternion(relative_yaw)
        imu.orientation_covariance[0] = imu.orientation_covariance[4] = imu.orientation_covariance[8] = 0.01
        imu.angular_velocity.z = w; imu.angular_velocity_covariance[0] = imu.angular_velocity_covariance[4] = imu.angular_velocity_covariance[8] = 0.01
        imu.linear_acceleration.z = 9.81; imu.linear_acceleration_covariance[0] = imu.linear_acceleration_covariance[4] = imu.linear_acceleration_covariance[8] = 0.1
        self.imu_pub.publish(imu)

    def scan(self):
        cfg = self.scan_cfg; count = int(cfg['count']); laser_yaw = self.yaw + float(self.robot['laser_yaw'])
        lx = self.x + float(self.robot['laser_x']) * math.cos(self.yaw); ly = self.y + float(self.robot['laser_x']) * math.sin(self.yaw)
        msg = LaserScan(); msg.header.stamp = self.get_clock().now().to_msg(); msg.header.frame_id = 'laser'
        msg.angle_min = -math.pi; msg.angle_increment = 2 * math.pi / count; msg.angle_max = msg.angle_min + (count - 1) * msg.angle_increment
        msg.range_min = float(cfg['min_range']); msg.range_max = float(cfg['max_range']); msg.scan_time = 1.0 / float(cfg['rate_hz']); msg.time_increment = 0.0
        msg.ranges = [self.maze.ray(lx, ly, laser_yaw + msg.angle_min + i * msg.angle_increment, msg.range_min, msg.range_max) for i in range(count)]
        self.latest_scan = [(lx + r * math.cos(laser_yaw + msg.angle_min + i * msg.angle_increment), ly + r * math.sin(laser_yaw + msg.angle_min + i * msg.angle_increment)) for i, r in enumerate(msg.ranges) if math.isfinite(r)]
        self.scan_pub.publish(msg)

    def audit(self):
        """Retain truth versus localization evidence for later failures."""
        record = {'time': self.get_clock().now().nanoseconds / 1e9,
                  'truth': [self.x, self.y, self.yaw],
                  'command': [self.v, self.w], 'actual_velocity': self.actual_velocity,
                  'blocked': self.blocked}
        try:
            transform = self.tf_buffer.lookup_transform('map', 'base_link', Time())
            t = transform.transform.translation
            record['localized_xy'] = [t.x, t.y]
            record['position_error'] = math.hypot(t.x - self.x, t.y - self.y)
        except TransformException:
            record['localized_xy'] = None
        self.trace.write(json.dumps(record) + '\n')
        self.trace.flush()


class Window:
    def __init__(self, simulator):
        import tkinter as tk
        from PIL import ImageTk
        self.tk = tk; self.sim = simulator; self.root = tk.Tk(); self.root.title('RB3302 simulator — ROS domain 86')
        self.pixel_scale = float(simulator.cfg.get('window', {}).get('scale', 150)) * simulator.maze.resolution
        landmarks = ROOT.parent / 'student_ws/src/competition_manager/config/landmarks.yaml'
        self.landmarks = yaml.safe_load(landmarks.read_text())['letters']
        image = simulator.maze.image.resize((round(simulator.maze.width * self.pixel_scale), round(simulator.maze.height * self.pixel_scale)), Image.Resampling.NEAREST)
        self.map_image = ImageTk.PhotoImage(image)
        self.canvas = tk.Canvas(self.root, width=image.width, height=image.height, background='gray'); self.canvas.pack()
        self.label = tk.Label(self.root, font=('sans', 11), anchor='w'); self.label.pack(fill='x')
        self.root.protocol('WM_DELETE_WINDOW', self.root.destroy)
        self.render()

    def render(self):
        s = self.sim; m = s.maze; c = self.canvas; c.delete('all'); c.create_image(0, 0, image=self.map_image, anchor='nw')
        for letter, (lx, ly) in self.landmarks.items():
            px, py = m.point(lx, ly, self.pixel_scale)
            c.create_text(px, py, text=letter, fill='#777777', font=('sans', 10, 'bold'))
        for x, y in s.latest_scan[::3]:
            px, py = m.point(x, y, self.pixel_scale); c.create_oval(px-1, py-1, px+1, py+1, fill='#ff3939', outline='')
        x, y = m.point(s.x, s.y, self.pixel_scale); ca, sa = math.cos(s.yaw), math.sin(s.yaw)
        points = []
        for dx, dy in [(-s.robot['length']/2,-s.robot['width']/2),(s.robot['length']/2,-s.robot['width']/2),(s.robot['length']/2,s.robot['width']/2),(-s.robot['length']/2,s.robot['width']/2)]:
            points.extend(m.point(s.x + ca*dx-sa*dy, s.y+sa*dx+ca*dy, self.pixel_scale))
        c.create_polygon(*points, fill='#2477cb', outline='#00447b', width=2)
        ex, ey = m.point(s.x + 0.17*ca, s.y + 0.17*sa, self.pixel_scale); c.create_line(x,y,ex,ey,fill='yellow',width=3,arrow='last')
        self.label.config(text=f'x={s.x:.2f}  y={s.y:.2f}  yaw={math.degrees(s.yaw):.1f}°  cmd=({s.v:.2f}, {s.w:.2f})' + ('  WALL CONTACT' if s.blocked else ''))
        self.root.after(80, self.render)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--config', default=str(ROOT / 'config.yaml')); parser.add_argument('--map', default=str(ROOT / 'maps/rb3302_map.yaml')); parser.add_argument('--headless', action='store_true'); args = parser.parse_args()
    config = yaml.safe_load(Path(args.config).read_text()); maze = Maze(args.map)
    rclpy.init(); simulator = Simulator(config, maze); window = None
    try:
        if not args.headless: window = Window(simulator)
        while rclpy.ok():
            rclpy.spin_once(simulator, timeout_sec=0.005)
            if window:
                try: window.root.update()
                except window.tk.TclError: break
    except KeyboardInterrupt:
        pass
    finally:
        if window:
            try: window.root.destroy()
            except window.tk.TclError: pass
        simulator.trace.close()
        simulator.destroy_node(); rclpy.try_shutdown()

if __name__ == '__main__': main()
