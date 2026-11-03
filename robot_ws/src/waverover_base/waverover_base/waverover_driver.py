#!/usr/bin/env python3

import json
import math
import threading
import time
import subprocess
from collections import deque

from diagnostic_msgs.msg import DiagnosticArray, DiagnosticStatus, KeyValue
from waverover_base.feedback import FeedbackTracker, MotionGate, finite
from waverover_base.device_lock import DeviceLock, existing_device_users

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TransformStamped, Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import BatteryState
from std_msgs.msg import String, Float32, Float32MultiArray, Int32MultiArray
from tf2_ros import TransformBroadcaster

import serial


class DisplayServiceGuard:
    def __init__(self, service_name: str, logger):
        self.service_name = service_name
        self.logger = logger
        self.stopped_by_us = False

    def stop(self):
        state = subprocess.run(
            ["systemctl", "is-active", self.service_name], capture_output=True,
            text=True, check=False, timeout=5.0)
        if state.returncode in (3, 4):
            return
        if state.returncode != 0:
            raise RuntimeError(f"Cannot determine service ownership: {state.stderr.strip()}")
        result = subprocess.run(
            ["sudo", "-n", "/bin/systemctl", "stop", self.service_name],
            capture_output=True, text=True, check=False, timeout=5.0)
        if result.returncode != 0:
            raise RuntimeError(f"Cannot stop competing service: {result.stderr.strip()}")
        self.stopped_by_us = True
        self.logger.info(f"Stopped {self.service_name}")

    def start(self):
        if not self.stopped_by_us:
            return
        try:
            result = subprocess.run(
                ["sudo", "-n", "/bin/systemctl", "start", self.service_name],
                capture_output=True,
                text=True,
                check=False,
                timeout=5.0,
            )
            if result.returncode == 0:
                self.logger.info(f"Restarted {self.service_name}")
                self.stopped_by_us = False
            else:
                self.logger.warning(f"Could not restart {self.service_name}: {result.stderr.strip()}")
        except Exception as exc:
            self.logger.warning(f"Failed to restart {self.service_name}: {exc}")


class SerialTransport:
    def __init__(self, port: str, baud: int, timeout: float, logger):
        self.port = port
        self.baud = baud
        self.timeout = timeout
        self.logger = logger
        self.ser = None
        self.io_lock = threading.RLock()
        self.read_buffer = bytearray()

    def open(self) -> bool:
        try:
            owners = existing_device_users(self.port)
            if owners:
                self.logger.error(f"Device already open by processes {owners}; refusing serial initialization")
                return False
            self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout, write_timeout=0.2, exclusive=True)
            time.sleep(2.0)
            self.ser.reset_input_buffer()
            self.ser.reset_output_buffer()
            self.logger.info(f"Opened serial port {self.port} at {self.baud} baud")
            return True
        except (serial.SerialException, OSError) as exc:
            self.logger.error(f"Failed to open serial port {self.port}: {exc}")
            return False

    def close(self):
        with self.io_lock:
            if self.ser and self.ser.is_open:
                self.ser.close()

    def write_json(self, cmd: dict):
        if not self.ser or not self.ser.is_open:
            return
        line = json.dumps(cmd, separators=(",", ":")) + "\n"
        with self.io_lock:
            try:
                self.ser.write(line.encode("utf-8"))
                return True
            except (serial.SerialException, OSError) as exc:
                self.logger.warning(f"Serial write error: {exc}")
                return False

    def send_cmd(self, cmd: dict) -> dict:
        if not self.ser or not self.ser.is_open:
            return {}
        line = json.dumps(cmd, separators=(",", ":")) + "\n"
        with self.io_lock:
            try:
                self.ser.write(line.encode("utf-8"))
                self.ser.flush()
                deadline = time.time() + self.timeout
                while time.time() < deadline:
                    raw = self.ser.readline().decode("utf-8", errors="ignore").strip()
                    if raw.startswith("{"):
                        try:
                            return json.loads(raw)
                        except json.JSONDecodeError:
                            continue
            except (serial.SerialException, OSError) as exc:
                self.logger.warning(f"Serial send error: {exc}")
        return {}

    def read_json_line(self) -> dict:
        if not self.ser or not self.ser.is_open:
            return {}
        with self.io_lock:
            # Read only available bytes: a partial line must never hold up stop commands.
            count = min(self.ser.in_waiting, 65536)
            if count:
                self.read_buffer.extend(self.ser.read(count))
            if len(self.read_buffer) > 65536:
                self.read_buffer.clear()
                raise ValueError("Serial receive buffer overflow")
            end = self.read_buffer.find(b"\n")
            if end < 0:
                return {}
            raw = bytes(self.read_buffer[:end])
            del self.read_buffer[:end + 1]
        try:
            result = json.loads(raw)
            return result if isinstance(result, dict) else {}
        except (json.JSONDecodeError, UnicodeDecodeError):
            return {}


class WaveRoverDriver(Node):
    def __init__(self):
        super().__init__("waverover_driver")

        self.declare_parameter("serial_port", "/dev/waverover")
        self.declare_parameter("baud_rate", 115200)
        self.declare_parameter("serial_timeout", 0.05)
        self.declare_parameter("max_linear_vel", 1.0)
        self.declare_parameter("max_angular_vel", 2.0)
        self.declare_parameter("cmd_vel_timeout", 0.8)
        self.declare_parameter("heartbeat_rate", 20.0)
        self.declare_parameter("load_calib_on_start", True)
        self.declare_parameter("rezero_imu_on_start", False)
        self.declare_parameter("heartbeat_delay_ms", 3000)
        self.declare_parameter("publish_odom", True)
        self.declare_parameter("publish_odom_tf", False)
        self.declare_parameter("odom_topic", "odom/raw")
        self.declare_parameter("odom_frame", "odom")
        self.declare_parameter("base_frame", "base_link")

        self.declare_parameter("feedback_rate", 100.0)
        self.declare_parameter("feedback_interval_ms", 10)
        self.declare_parameter("battery_rate", 1.0)
        self.declare_parameter("display_update_rate", 1.0)

        self.declare_parameter("battery_full_voltage", 12.6)
        self.declare_parameter("battery_empty_voltage", 9.0)
        self.declare_parameter("low_battery_percentage", 20.0)
        self.declare_parameter("very_low_battery_percentage", 10.0)

        self.declare_parameter("show_battery_percentage", True)
        self.declare_parameter("display_line_num", 4)
        self.declare_parameter("very_low_flash_rate", 2.0)

        self.serial_port = self.get_parameter("serial_port").value
        self.baud_rate = self.get_parameter("baud_rate").value
        self.serial_timeout = self.get_parameter("serial_timeout").value
        self.max_linear_vel = self.get_parameter("max_linear_vel").value
        self.max_angular_vel = self.get_parameter("max_angular_vel").value
        self.cmd_vel_timeout = self.get_parameter("cmd_vel_timeout").value
        self.heartbeat_rate = self.get_parameter("heartbeat_rate").value
        self.load_calib_on_start = self.get_parameter("load_calib_on_start").value
        self.rezero_imu_on_start = self.get_parameter("rezero_imu_on_start").value
        self.heartbeat_delay_ms = self.get_parameter("heartbeat_delay_ms").value
        self.publish_odom = self.get_parameter("publish_odom").value
        self.publish_odom_tf = self.get_parameter("publish_odom_tf").value
        self.odom_topic = self.get_parameter("odom_topic").value
        self.odom_frame = self.get_parameter("odom_frame").value
        self.base_frame = self.get_parameter("base_frame").value

        self.feedback_rate = self.get_parameter("feedback_rate").value
        self.feedback_interval_ms = self.get_parameter("feedback_interval_ms").value
        self.battery_rate = self.get_parameter("battery_rate").value
        self.display_update_rate = self.get_parameter("display_update_rate").value

        self.battery_full_voltage = self.get_parameter("battery_full_voltage").value
        self.battery_empty_voltage = self.get_parameter("battery_empty_voltage").value
        self.low_battery_percentage = self.get_parameter("low_battery_percentage").value
        self.very_low_battery_percentage = self.get_parameter("very_low_battery_percentage").value

        self.show_battery_percentage = self.get_parameter("show_battery_percentage").value
        self.display_line_num = self.get_parameter("display_line_num").value
        self.very_low_flash_rate = self.get_parameter("very_low_flash_rate").value

        settings = {
            "feedback_timeout_sec": 0.5, "feedback_max_gap_sec": 0.5,
            "odom_distance_source": "firmware_centre", "yaw_odom_unit": "radians",
            "wheel_track_width": 0.125, "wheel_yaw_rate_enabled": False,
            "feedback_sequence_field": "", "max_feedback_wheel_speed": 1.5,
            "max_feedback_yaw_rate": 12.0, "odom_linear_variance": 0.0025,
            "odom_wheel_yaw_rate_variance": 0.04, "firmware_main_type": 1,
            "firmware_module_type": 0, "diagnostic_rate": 2.0,
        }
        for key, value in settings.items():
            self.declare_parameter(key, value)
            setattr(self, key, self.get_parameter(key).value)
        for key in ("feedback_timeout_sec", "feedback_max_gap_sec", "odom_linear_variance",
                    "odom_wheel_yaw_rate_variance", "diagnostic_rate", "heartbeat_rate",
                    "feedback_rate", "cmd_vel_timeout", "max_linear_vel", "max_angular_vel"):
            if not finite(getattr(self, key)) or getattr(self, key) <= 0:
                raise ValueError(f"{key} must be finite and positive")
        for key in ('firmware_main_type', 'firmware_module_type'):
            value = getattr(self, key)
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= 255:
                raise ValueError(f'{key} must be an integer in [0, 255]')
        self.tracker = FeedbackTracker(
            source=self.odom_distance_source, yaw_unit=self.yaw_odom_unit,
            max_gap=self.feedback_max_gap_sec, max_wheel_speed=self.max_feedback_wheel_speed,
            max_yaw_rate=self.max_feedback_yaw_rate, track_width=self.wheel_track_width,
            wheel_yaw_rate_enabled=self.wheel_yaw_rate_enabled,
            sequence_field=self.feedback_sequence_field)
        self.motion_gate = MotionGate(self.max_linear_vel, self.max_angular_vel)
        self.command_lock = threading.RLock()
        self.pending_samples = deque(maxlen=200)
        self.pending_raw = deque(maxlen=200)
        self.dropped_samples = 0
        self.last_ros_sample = None
        self.transport = None
        self.display_service = None
        self.reader_thread = None
        self._hardware_closed = False
        self.device_lock = DeviceLock(self.serial_port)
        self.current_linear = 0.0
        self.current_angular = 0.0
        self.last_cmd_vel_time = self.get_clock().now()

        self.feedback_lock = threading.Lock()
        self.latest_json_feedback = "{}"
        self.dist_L = 0.0
        self.dist_R = 0.0
        self.dist_centre = 0.0
        self.yaw_odom = 0.0
        self.yaw_imu = 0.0
        self.imu_roll = 0.0
        self.imu_pitch = 0.0
        self.voltage = 0.0
        self.battery_percentage = 0.0
        self.enc_A = 0
        self.enc_B = 0
        self.odom_x = 0.0
        self.odom_y = 0.0
        self.prev_dist_centre = None
        self.prev_odom_time = self.get_clock().now()
        self.running = True
        self.display_flash_on = True
        self.display_update_count = 0

        # Acquire before ANY service or device mutation. A losing instance does no cleanup.
        try:
            self.device_lock.acquire()
        except BaseException:
            super().destroy_node()
            raise
        try:
            self.display_service = DisplayServiceGuard("waverover-init.service", self.get_logger())
            self.display_service.stop()
            time.sleep(0.5)

            self.transport = SerialTransport(self.serial_port, self.baud_rate, self.serial_timeout, self.get_logger())
            if not self.transport.open():
                raise RuntimeError("Serial port could not be opened exclusively")

            self._initialize_robot()

            self.create_subscription(Twist, "cmd_vel", self._cmd_vel_callback, 10)

            self.json_feedback_pub = self.create_publisher(String, "waverover/json_feedback", 10)
            self.raw_feedback_pub = self.create_publisher(Float32MultiArray, "waverover/raw_feedback", 10)
            self.encoder_pub = self.create_publisher(Int32MultiArray, "encoders", 10)
            self.battery_pub = self.create_publisher(BatteryState, "battery", 10)
            self.battery_percentage_pub = self.create_publisher(Float32, "battery_percentage", 10)
            self.odom_pub = self.create_publisher(Odometry, self.odom_topic, 10)
            self.tf_broadcaster = TransformBroadcaster(self)
            self.diagnostic_pub = self.create_publisher(DiagnosticArray, "diagnostics", 10)
            self.driver_diagnostic_pub = self.create_publisher(String, "waverover/driver_diagnostics", 10)

            self.create_timer(1.0 / self.heartbeat_rate, self._heartbeat_callback)
            self.create_timer(1.0 / self.feedback_rate, self._feedback_publish_callback)
            self.create_timer(1.0 / self.diagnostic_rate, self._diagnostic_callback)
            self.create_timer(1.0 / self.battery_rate, self._battery_publish_callback)
            self.create_timer(1.0 / self.display_update_rate, self._battery_display_callback)

            self.reader_thread = threading.Thread(target=self._serial_reader_loop, daemon=True)
            self.reader_thread.start()

            self._send_display_text("BAT --%", force=True)
            self.get_logger().info("WAVE ROVER driver started")

        except BaseException:
            try:
                self._cleanup_hardware()
            finally:
                super().destroy_node()
            raise

    def _initialize_robot(self):
        self.get_logger().info("Initializing WAVE ROVER base")
        self.transport.send_cmd({"T": 900, "main": int(self.firmware_main_type), "module": int(self.firmware_module_type)})
        time.sleep(0.2)

        if self.load_calib_on_start:
            self.transport.send_cmd({"T": 161})
            time.sleep(0.2)

        if self.rezero_imu_on_start:
            self.get_logger().info("Re-zeroing IMU")
            time.sleep(2.0)
            self.transport.send_cmd({"T": 127})
            time.sleep(0.2)

        self.transport.send_cmd({"T": 151})
        time.sleep(0.2)
        self.transport.send_cmd({"T": 136, "cmd": self.heartbeat_delay_ms})
        time.sleep(0.1)
        self.transport.send_cmd({"T": 142, "cmd": int(self.feedback_interval_ms)})
        time.sleep(0.1)
        self.transport.send_cmd({"T": 131, "cmd": 1})
        time.sleep(0.1)
        self.transport.send_cmd({"T": 143, "cmd": 0})
        time.sleep(0.1)
        self._send_velocity(0.0, 0.0)

    def _feedback_ready(self, now):
        with self.feedback_lock:
            return self.tracker.ready(now, self.feedback_timeout_sec)

    def _cmd_vel_callback(self, msg: Twist):
        now = time.monotonic()
        with self.command_lock:
            command = self.motion_gate.receive(msg.linear.x, msg.angular.z, now,
                                               self._feedback_ready(now))
            self.current_linear, self.current_angular = command
            self._send_velocity(*command)

    def _heartbeat_callback(self):
        now = time.monotonic()
        with self.command_lock:
            command = self.motion_gate.output(now, self.cmd_vel_timeout, self._feedback_ready(now))
            self.current_linear, self.current_angular = command
            self._send_velocity(*command)

    def _send_velocity(self, linear: float, angular: float):
        if not self.transport or not self.transport.ser or not self.transport.ser.is_open:
            return False
        ok = self.transport.write_json({"T": 13, "X": round(linear, 4), "Z": round(angular, 4)})
        if not ok:
            self.motion_gate.invalidate("serial_write_failed")
        return ok

    def _serial_reader_loop(self):
        while self.running:
            try:
                data = self.transport.read_json_line()
                if data:
                    self._process_feedback(data)
                else:
                    time.sleep(0.002)
            except Exception as exc:
                self.get_logger().warning(f"Serial read loop error: {exc}")
                time.sleep(0.5)

    def _process_feedback(self, data: dict):
        received = time.monotonic()
        stamp = self.get_clock().now().to_msg()
        with self.feedback_lock:
            if len(self.pending_raw) == self.pending_raw.maxlen:
                self.dropped_samples += 1
            self.pending_raw.append(json.dumps(data, separators=(",", ":")))
            if data.get('T') == 1001:
                ros_seconds = stamp.sec + stamp.nanosec / 1e9
                prior = self.last_ros_sample
                self.last_ros_sample = (ros_seconds, received)
                if prior is not None and (ros_seconds < prior[0] or
                        abs((ros_seconds-prior[0]) - (received-prior[1])) > self.feedback_max_gap_sec):
                    self.tracker.reset('ros_clock_jump')
                    self.pending_samples.clear()
                    return
            sample = self.tracker.update(data, received)
            if data.get("T") == 1001 and self.tracker.last_error in ("", "baseline_only"):
                for attr, key in (("dist_L", "dist_L"), ("dist_R", "dist_R"),
                                  ("dist_centre", "dist_centre"), ("yaw_odom", "yaw_odom"),
                                  ("voltage", "voltage"), ("enc_A", "encA"), ("enc_B", "encB")):
                    setattr(self, attr, data[key])
                self.battery_percentage = self._estimate_battery_percentage(self.voltage)
            for attr, key in (("yaw_imu", "yaw_imu"), ("imu_roll", "r"), ("imu_pitch", "p")):
                if finite(data.get(key)):
                    setattr(self, attr, data[key])
            if sample is not None:
                if len(self.pending_samples) == self.pending_samples.maxlen:
                    self.dropped_samples += 1
                self.pending_samples.append((stamp, received, sample))

    def _estimate_battery_percentage(self, voltage: float) -> float:
        if voltage <= 0.01:
            return 0.0
        span = self.battery_full_voltage - self.battery_empty_voltage
        if span <= 0.01:
            return 0.0
        pct = (voltage - self.battery_empty_voltage) / span * 100.0
        return max(0.0, min(100.0, pct))

    def _feedback_publish_callback(self):
        with self.feedback_lock:
            raw_packets = list(self.pending_raw)
            self.pending_raw.clear()
            samples = list(self.pending_samples)
            self.pending_samples.clear()
            ready = self.tracker.ready(time.monotonic(), self.feedback_timeout_sec)
            raw_values = [float(self.dist_L), float(self.dist_R), float(self.dist_centre),
                          float(self.yaw_odom), float(self.yaw_imu), float(self.imu_roll),
                          float(self.imu_pitch), float(self.voltage), float(self.battery_percentage)]
            encoders = [int(self.enc_A), int(self.enc_B)]
        for text in raw_packets:
            msg = String()
            msg.data = text
            self.json_feedback_pub.publish(msg)
        if samples and ready:
            raw_msg = Float32MultiArray()
            raw_msg.data = raw_values
            self.raw_feedback_pub.publish(raw_msg)
            enc_msg = Int32MultiArray()
            enc_msg.data = encoders
            self.encoder_pub.publish(enc_msg)
            if self.publish_odom:
                for stamp, received, sample in samples:
                    if 0 <= time.monotonic() - received <= self.feedback_timeout_sec:
                        self._publish_odom(stamp, sample)

    def _publish_odom(self, stamp, sample):
        msg = Odometry()
        msg.header.stamp = stamp
        msg.header.frame_id = self.odom_frame
        msg.child_frame_id = self.base_frame
        msg.pose.pose.position.x, msg.pose.pose.position.y = sample['x'], sample['y']
        msg.pose.pose.orientation.z = math.sin(sample['yaw'] / 2)
        msg.pose.pose.orientation.w = math.cos(sample['yaw'] / 2)
        msg.twist.twist.linear.x = sample['linear_velocity']
        # Zero is only a placeholder when invalid, never a stationary measurement.
        msg.twist.twist.angular.z = sample['angular_velocity']
        for i in (0, 7, 14, 21, 28, 35):
            msg.pose.covariance[i] = 1e6
            msg.twist.covariance[i] = 1e6
        msg.twist.covariance[0] = self.odom_linear_variance
        if sample['yaw_rate_valid']:
            msg.twist.covariance[35] = self.odom_wheel_yaw_rate_variance
        self.odom_pub.publish(msg)
        if self.publish_odom_tf:
            tr = TransformStamped()
            tr.header = msg.header
            tr.child_frame_id = self.base_frame
            tr.transform.translation.x, tr.transform.translation.y = sample['x'], sample['y']
            tr.transform.rotation = msg.pose.pose.orientation
            self.tf_broadcaster.sendTransform(tr)

    def _diagnostic_callback(self):
        now = time.monotonic()
        with self.command_lock:
            with self.feedback_lock:
                ready = self.tracker.ready(now, self.feedback_timeout_sec)
                age = now - self.tracker.last_valid if self.tracker.last_valid is not None else None
                details = dict(self.tracker.latest or {})
                details.update(feedback_ready=ready, feedback_age_sec=age,
                               feedback_received_age_sec=(now-self.tracker.last_received
                                   if self.tracker.last_received is not None else None),
                               feedback_sequence=self.tracker.sequence,
                               invalid_count=self.tracker.invalid_count, reset_count=self.tracker.reset_count,
                               feedback_error=self.tracker.last_error, dropped_samples=self.dropped_samples,
                               distance_source=self.odom_distance_source, yaw_unit=self.yaw_odom_unit,
                               timestamp_source='host_monotonic_receive',
                               linear_variance=self.odom_linear_variance,
                               wheel_yaw_rate_enabled=self.wheel_yaw_rate_enabled,
                               requested_velocity=list(self.motion_gate.command),
                               motion_gate=self.motion_gate.reason,
                               firmware_main_type=self.firmware_main_type,
                               firmware_module_type=self.firmware_module_type)
        text = String()
        text.data = json.dumps(details, allow_nan=False)
        self.driver_diagnostic_pub.publish(text)
        status = DiagnosticStatus()
        status.name = self.get_fully_qualified_name() + '/feedback'
        status.hardware_id = self.serial_port
        status.level = DiagnosticStatus.OK if ready else DiagnosticStatus.ERROR
        status.message = 'fresh measured feedback' if ready else 'motion inhibited: feedback unavailable'
        status.values = [KeyValue(key=k, value=json.dumps(v)) for k, v in details.items()]
        msg = DiagnosticArray()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.status = [status]
        self.diagnostic_pub.publish(msg)

    def _battery_publish_callback(self):
        with self.feedback_lock:
            voltage = float(self.voltage)
            percent = float(self.battery_percentage)

        battery_msg = BatteryState()
        battery_msg.header.stamp = self.get_clock().now().to_msg()
        battery_msg.voltage = voltage
        battery_msg.percentage = percent / 100.0
        battery_msg.present = True
        battery_msg.power_supply_status = BatteryState.POWER_SUPPLY_STATUS_DISCHARGING
        battery_msg.power_supply_health = BatteryState.POWER_SUPPLY_HEALTH_UNKNOWN
        battery_msg.power_supply_technology = BatteryState.POWER_SUPPLY_TECHNOLOGY_LION
        self.battery_pub.publish(battery_msg)

        pct_msg = Float32()
        pct_msg.data = percent
        self.battery_percentage_pub.publish(pct_msg)

    def _battery_display_callback(self):
        if not self.show_battery_percentage:
            return

        with self.feedback_lock:
            percent = float(self.battery_percentage)
            voltage = float(self.voltage)

        if voltage <= 0.01:
            self._send_display_text("BAT --%", force=True)
            return

        pct_int = int(round(percent))

        if percent <= self.very_low_battery_percentage:
            self.display_update_count += 1
            self.display_flash_on = not self.display_flash_on
            text = f"CRIT {pct_int}%" if self.display_flash_on else ""
            self._send_display_text(text, force=True)
            return

        if percent <= self.low_battery_percentage:
            self._send_display_text(f"LOW {pct_int}%", force=True)
            return

        self._send_display_text(f"BAT {pct_int}%", force=True)

    def _send_display_text(self, text: str, force: bool = False):
        # Always force for display reliability because other firmware/UI tasks may repaint the line.
        self.transport.write_json({"T": 3, "lineNum": int(self.display_line_num), "Text": str(text)})

    def _cleanup_hardware(self):
        if self._hardware_closed:
            return
        self._hardware_closed = True
        self.running = False
        try:
            try:
                with self.command_lock:
                    self.motion_gate.invalidate("shutdown")
                    if self.transport and self.transport.ser and self.transport.ser.is_open:
                        self._send_velocity(0., 0.)
                        self.transport.write_json({"T": 131, "cmd": 0})
                if self.reader_thread and self.reader_thread.is_alive():
                    self.reader_thread.join(timeout=1.)
            finally:
                try:
                    if self.transport:
                        self.transport.close()
                finally:
                    if self.display_service:
                        self.display_service.start()
        finally:
            self.device_lock.close()

    def destroy_node(self):
        self.get_logger().info("Stopping WAVE ROVER")
        try:
            self._cleanup_hardware()
        finally:
            super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = None
    try:
        node = WaveRoverDriver()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        rclpy.try_shutdown()


if __name__ == "__main__":
    main()
