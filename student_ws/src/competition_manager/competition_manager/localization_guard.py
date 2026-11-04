"""Stationary AMCL refinement and independent scan/map readiness checks."""
from collections import deque
import math
import time

from geometry_msgs.msg import PoseWithCovarianceStamped, Twist
from nav_msgs.msg import OccupancyGrid
from nav2_msgs.srv import ClearEntireCostmap
from rclpy.qos import DurabilityPolicy, QoSProfile, qos_profile_sensor_data
from rclpy.time import Time
from sensor_msgs.msg import LaserScan
from std_srvs.srv import Empty
from tf2_ros import TransformException


DEFAULTS = {
    'localization_timeout_sec': 30.0, 'localization_update_interval_sec': 0.5,
    'localization_max_updates': 40, 'localization_pose_timeout_sec': 2.0,
    'localization_max_xy_stddev': 0.15, 'localization_max_yaw_stddev': 0.20,
    'localization_match_distance': 0.10, 'localization_min_match_ratio': 0.80,
    'localization_stable_samples': 3, 'localization_stable_xy': 0.04,
    'localization_stable_yaw': 0.05,
}


class LocalizationFailed(RuntimeError):
    """Localization was not verified; stay stopped and ask for a measured pose."""


def pose_values(message):
    p, q = message.pose.pose.position, message.pose.pose.orientation
    return p.x, p.y, math.atan2(2*(q.w*q.z+q.x*q.y), 1-2*(q.y*q.y+q.z*q.z))


def covariance_ok(message, max_xy, max_yaw):
    c = message.pose.covariance
    # Largest eigenvalue of the XY covariance, including correlation.
    a, b, d, angular = c[0], (c[1]+c[6])/2, c[7], c[35]
    if not all(math.isfinite(v) for v in (a, b, d, angular)):
        return False
    if min(a, d, angular) < 0 or a*d-b*b < -1e-10:
        return False
    eigen = (a+d+math.sqrt((a-d)**2+4*b*b))/2
    return eigen <= max_xy**2 and angular <= max_yaw**2


def stable(poses, xy_limit, yaw_limit):
    if not poses or not all(math.isfinite(v) for p in poses for v in p):
        return False
    # Compare all pairs, including angles across the +/-pi boundary.
    return all(math.hypot(a[0]-b[0], a[1]-b[1]) <= xy_limit
               and abs(math.atan2(math.sin(a[2]-b[2]), math.cos(a[2]-b[2]))) <= yaw_limit
               for a in poses for b in poses)


def scan_match(scan, transform, grid, distance, max_samples=80):
    """Fraction of finite endpoints near occupied cells; unknown is not a wall."""
    valid = [(i, r) for i, r in enumerate(scan.ranges)
             if math.isfinite(r) and scan.range_min <= r <= scan.range_max]
    if len(valid) < 20:
        return 0.0
    valid = valid[::max(1, math.ceil(len(valid)/max_samples))]
    q, t = transform.rotation, transform.translation
    # Full quaternion rotation: laser mounting may include a roll/pitch flip.
    r00, r01 = 1-2*(q.y*q.y+q.z*q.z), 2*(q.x*q.y-q.w*q.z)
    r10, r11 = 2*(q.x*q.y+q.w*q.z), 1-2*(q.x*q.x+q.z*q.z)
    info = grid.info
    oq = info.origin.orientation
    angle = math.atan2(2*(oq.w*oq.z+oq.x*oq.y), 1-2*(oq.y*oq.y+oq.z*oq.z))
    c, s = math.cos(angle), math.sin(angle)
    radius = math.ceil(distance/info.resolution)+1
    matches = 0
    for i, length in valid:
        angle = scan.angle_min+i*scan.angle_increment
        lx, ly = length*math.cos(angle), length*math.sin(angle)
        x = t.x+r00*lx+r01*ly-info.origin.position.x
        y = t.y+r10*lx+r11*ly-info.origin.position.y
        x, y = c*x+s*y, -s*x+c*y
        ix, iy = math.floor(x/info.resolution), math.floor(y/info.resolution)
        hit = False
        for cy in range(max(0, iy-radius), min(info.height, iy+radius+1)):
            for cx in range(max(0, ix-radius), min(info.width, ix+radius+1)):
                if (grid.data[cy*info.width+cx] >= 65
                        and math.hypot((cx+.5)*info.resolution-x,
                                       (cy+.5)*info.resolution-y) <= distance):
                    hit = True
                    break
            if hit:
                break
        matches += hit
    return matches/len(valid)


class LocalizationGuard:
    """Mixin for the mission owner: never reset pose or publish drive commands."""

    def _init_localization(self):
        self._loc_pose = self._loc_scan = self._loc_map = None
        self._loc_history = deque(maxlen=self.p('localization_stable_samples'))
        self._loc_matched_scans = deque(maxlen=3)
        self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose',
                                 self._localization_pose_callback, qos_profile_sensor_data)
        self.create_subscription(LaserScan, '/scan', self._localization_scan_callback,
                                 qos_profile_sensor_data)
        self.create_subscription(OccupancyGrid, '/map', self._localization_map_callback,
                                 QoSProfile(depth=1, durability=DurabilityPolicy.TRANSIENT_LOCAL))

    def _localization_pose_callback(self, msg):
        # Duplicate stamps must not count as consecutive fresh filter updates.
        key = (msg.header.stamp.sec, msg.header.stamp.nanosec)
        if self._loc_pose is not None and key <= self._loc_pose[2]:
            return
        if covariance_ok(msg, self.p('localization_max_xy_stddev'),
                         self.p('localization_max_yaw_stddev')):
            self._loc_history.append(pose_values(msg))
        else:
            self._loc_history.clear()
        self._loc_pose = (time.monotonic(), msg, key)

    def _localization_scan_callback(self, msg):
        self._loc_scan = (time.monotonic(), msg)

    def _localization_map_callback(self, msg):
        if (msg.info.resolution > 0 and msg.info.width > 0 and msg.info.height > 0
                and len(msg.data) == msg.info.width*msg.info.height):
            self._loc_map = msg

    def _localization_quality(self):
        now = time.monotonic()
        if not self._stationary() or self._current_pose() is None:
            return False, 'waiting for stopped robot and fresh TF/odometry'
        if (self._loc_pose is None or self._loc_scan is None or self._loc_map is None
                or now-self._loc_pose[0] > self.p('localization_pose_timeout_sec')
                or now-self._loc_scan[0] > self.p('telemetry_timeout_sec')):
            return False, 'waiting for fresh AMCL pose, scan and saved map'
        msg = self._loc_pose[1]
        q = msg.pose.pose.orientation
        norm = q.x*q.x+q.y*q.y+q.z*q.z+q.w*q.w
        if not math.isfinite(norm) or abs(norm-1.) > .1:
            return False, 'AMCL orientation is invalid'
        pose_age = (self.get_clock().now()-Time.from_msg(msg.header.stamp)).nanoseconds/1e9
        if pose_age < -0.1 or pose_age > self.p('localization_pose_timeout_sec'):
            return False, 'AMCL pose header is stale or in the future'
        if (msg.header.frame_id != self.p('map_frame')
                or self._loc_map.header.frame_id != self.p('map_frame')):
            return False, 'AMCL pose frame does not match map'
        cov = covariance_ok(msg, self.p('localization_max_xy_stddev'),
                            self.p('localization_max_yaw_stddev'))
        history_ok = (len(self._loc_history) == self.p('localization_stable_samples')
                      and stable(self._loc_history, self.p('localization_stable_xy'),
                                 self.p('localization_stable_yaw')))
        scan = self._loc_scan[1]
        age = (self.get_clock().now()-Time.from_msg(scan.header.stamp)).nanoseconds/1e9
        if age < -0.1 or age > self.p('telemetry_timeout_sec'):
            return False, 'scan header is stale or in the future'
        try:
            tf = self._tf.lookup_transform(self.p('map_frame'), scan.header.frame_id,
                                           Time.from_msg(scan.header.stamp))
        except TransformException:
            return False, 'scan-time TF unavailable'
        match = scan_match(scan, tf.transform, self._loc_map,
                           self.p('localization_match_distance'))
        if cov and history_ok and match >= self.p('localization_min_match_ratio'):
            key = (scan.header.stamp.sec, scan.header.stamp.nanosec)
            if not self._loc_matched_scans or key != self._loc_matched_scans[-1]:
                self._loc_matched_scans.append(key)
        else:
            self._loc_matched_scans.clear()
        good = cov and history_ok and len(self._loc_matched_scans) == 3
        return good, f'covariance_ok={cov}, stable={history_ok}, scan_match={match:.0%}'

    def _localization_service(self, service_type, name, until):
        client = self.create_client(service_type, name)
        future = None
        try:
            while not client.service_is_ready():
                if time.monotonic() >= until:
                    return False
                self._stop_pub.publish(Twist())
                self._spin()
            future = client.call_async(service_type.Request())
            while not future.done() and time.monotonic() < until:
                self._stop_pub.publish(Twist())
                self._spin()
            return future.done() and future.result() is not None
        finally:
            if future is not None and not future.done():
                client.remove_pending_request(future)
                future.cancel()
            self.destroy_client(client)

    def ensure_localization(self, force=False):
        if not force and self._localization_quality()[0]:
            self.get_logger().info('AMCL already verified; keeping current pose')
            return False
        self._loc_history.clear()
        self._loc_matched_scans.clear()
        until = time.monotonic()+self.p('localization_timeout_sec')
        next_update, updates, log_at = 0., 0, 0.
        detail = 'no fresh localization data'
        while time.monotonic() < until:
            self._check_deadline()
            self._stop_pub.publish(Twist())
            good, detail = self._localization_quality()
            if good:
                self.get_logger().info(f'AMCL verified after {updates} stationary updates: {detail}')
                return True
            now = time.monotonic()
            if now >= log_at:
                self.get_logger().info(f'AMCL refining while stopped: {detail}; updates={updates}')
                log_at = now+2.
            # Never ask AMCL to treat a moving robot as stationary.
            if self._stationary() and now >= next_update:
                if updates >= self.p('localization_max_updates'):
                    break
                updates += 1
                self._localization_service(Empty, '/request_nomotion_update', min(until, now+2.))
                next_update = time.monotonic()+self.p('localization_update_interval_sec')
            self._spin()
        raise LocalizationFailed('AMCL did not converge: '+detail+
                                 '; stay stopped and set the actual pose with RViz 2D Pose Estimate')

    def recover_localization(self, force=False):
        if self.ensure_localization(force=force):
            # Reproject observations only after the localization correction is stable.
            for service in ('global_costmap/clear_entirely_global_costmap',
                            'local_costmap/clear_entirely_local_costmap'):
                if not self._localization_service(ClearEntireCostmap, service,
                                                  time.monotonic()+3.):
                    raise LocalizationFailed('Localization verified but costmap refresh failed: '+service)
            self._wait_before_retry()
