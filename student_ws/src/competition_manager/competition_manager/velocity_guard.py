"""Final velocity gate: bounded commands, immediate stops and scan swept footprint."""
import math
import time

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import LaserScan
from std_srvs.srv import Trigger
from tf2_ros import Buffer, TransformException, TransformListener


def bound_axis(value, requested, limit):
    """Never amplify the request, retain the wrong sign, or ignore a zero."""
    if not all(math.isfinite(x) for x in (value, requested)) or value * requested <= 0:
        return 0.0
    return math.copysign(min(abs(value), abs(requested), limit), requested)


def swept_collision(points, v, w, horizon=.8, half_length=.12, half_width=.115):
    """Check laser endpoints against the padded rectangular swept body."""
    for i in range(17):
        t = horizon * i / 16
        yaw = w * t
        x = v * t if abs(w) < 1e-6 else v / w * math.sin(yaw)
        y = 0.0 if abs(w) < 1e-6 else v / w * (1 - math.cos(yaw))
        c, s = math.cos(yaw), math.sin(yaw)
        for px, py in points:
            dx, dy = px-x, py-y
            if abs(c*dx+s*dy) <= half_length and abs(-s*dx+c*dy) <= half_width:
                return True
    return False


class VelocityGuard(Node):
    """Only publisher of the final navigation velocity topic."""
    def __init__(self):
        super().__init__('velocity_guard')
        for name, value in {'base_frame': 'base_link', 'max_linear': .2,
                            'max_angular': 1.0, 'command_timeout': .3,
                            'scan_timeout': .5, 'horizon': .8}.items():
            self.declare_parameter(name, value)
        self.raw = self.smooth = None
        self.raw_at = self.smooth_at = self.scan_at = self.stop_at = -math.inf
        self.points = None
        self.buffer = Buffer()
        self.listener = TransformListener(self.buffer, self)
        self.pub = self.create_publisher(Twist, 'cmd_vel', 10)
        self.create_subscription(Twist, '/cmd_vel_nav_raw', self.request, 10)
        self.create_subscription(Twist, '/cmd_vel_smoothed', self.smoothed, 10)
        self.create_subscription(Twist, '/cmd_vel_stop', self.stop, 10)
        self.create_subscription(LaserScan, '/scan', self.scan, qos_profile_sensor_data)
        self.create_service(Trigger, '/velocity_guard/ready', self.ready)
        self.reason = None
        self.create_timer(.05, self.tick)

    def ready(self, request, response):
        del request
        response.success = self.points is not None and time.monotonic()-self.scan_at <= self.p('scan_timeout')
        response.message = 'ready' if response.success else 'Waiting for fresh scan and laser TF'
        return response

    def p(self, name):
        return self.get_parameter(name).value

    def request(self, msg):
        self.raw, self.raw_at = msg, time.monotonic()
        # A controller stop must not await smoother deceleration.
        if msg.linear.x == 0 and msg.angular.z == 0:
            self.pub.publish(Twist())

    def smoothed(self, msg):
        self.smooth, self.smooth_at = msg, time.monotonic()

    def stop(self, msg):
        del msg
        self.stop_at = time.monotonic()
        self.pub.publish(Twist())

    def scan(self, msg):
        self.points = None
        age = (self.get_clock().now() - Time.from_msg(msg.header.stamp)).nanoseconds / 1e9
        if age > self.p('scan_timeout') or age < -.1 or not msg.ranges:
            return
        try:
            tf = self.buffer.lookup_transform(self.p('base_frame'), msg.header.frame_id, Time())
        except TransformException:
            return
        q, tr = tf.transform.rotation, tf.transform.translation
        yaw = math.atan2(2*(q.w*q.z+q.x*q.y), 1-2*(q.y*q.y+q.z*q.z))
        self.points = [(tr.x+r*math.cos(yaw+msg.angle_min+i*msg.angle_increment),
                        tr.y+r*math.sin(yaw+msg.angle_min+i*msg.angle_increment))
                       for i, r in enumerate(msg.ranges)
                       if math.isfinite(r) and msg.range_min <= r <= msg.range_max]
        # NaNs/zero returns are not evidence of free space. +inf is a valid no-hit.
        if not any((math.isfinite(r) and msg.range_min <= r <= msg.range_max)
                   or r == math.inf for r in msg.ranges):
            self.points = None
            return
        self.scan_at = time.monotonic()

    def tick(self):
        now = time.monotonic()
        out = Twist()
        reason = 'clear'
        if now-self.stop_at < .3:
            reason = 'mission_stop'
        elif min(now-self.raw_at, now-self.smooth_at) < 0 or max(now-self.raw_at, now-self.smooth_at) > self.p('command_timeout'):
            reason = 'command_timeout'
        elif self.points is None or now-self.scan_at > self.p('scan_timeout'):
            reason = 'scan_unavailable'
        else:
            out.linear.x = bound_axis(self.smooth.linear.x, self.raw.linear.x, self.p('max_linear'))
            out.angular.z = bound_axis(self.smooth.angular.z, self.raw.angular.z, self.p('max_angular'))
            if swept_collision(self.points, out.linear.x, out.angular.z, self.p('horizon')):
                out = Twist()
                reason = 'obstacle_stop'
        self.pub.publish(out)
        if reason != self.reason:
            self.get_logger().info('Velocity gate: ' + reason)
            self.reason = reason


def main(args=None):
    rclpy.init(args=args)
    node = VelocityGuard()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.pub.publish(Twist())
        node.destroy_node()
        rclpy.try_shutdown()
