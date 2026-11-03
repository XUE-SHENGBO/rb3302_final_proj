from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package="waverover_base",
            executable="waverover_driver",
            name="waverover_driver",
            output="screen",
            parameters=[{
                "serial_port": "/dev/waverover",
                "baud_rate": 115200,
                "cmd_vel_timeout": 0.8,
                "heartbeat_rate": 20.0,
                "serial_timeout": 0.05,
                "feedback_timeout_sec": 0.5,
                "feedback_max_gap_sec": 0.5,
                # Keep the old source until wheel/centre semantics are calibrated.
                "odom_distance_source": "firmware_centre",
                "yaw_odom_unit": "radians",
                "wheel_yaw_rate_enabled": False,
                "wheel_track_width": 0.125,
                # Provisional measurement variances; refine from ground calibration.
                "odom_linear_variance": 0.0025,
                "odom_wheel_yaw_rate_variance": 0.04,
                "firmware_main_type": 1,
                "firmware_module_type": 0,
                "max_linear_vel": 0.8,
                "max_angular_vel": 3.0,
                "publish_odom": True,
                "publish_odom_tf": False,
                "odom_topic": "/odom/raw",
                "odom_frame": "odom",
                "base_frame": "base_link",
                "load_calib_on_start": True,
                "rezero_imu_on_start": False,

                "feedback_rate": 100.0,
                "feedback_interval_ms": 10,

                # Battery ROS topics are intentionally slow.
                "battery_rate": 1.0,

                # Display update is separate from /battery publishing.
                "display_update_rate": 1.0,
                "display_line_num": 3,
                "show_battery_percentage": True,

                # 3-cell 18650 pack.
                "battery_full_voltage": 12.6,
                "battery_empty_voltage": 9.0,
                "low_battery_percent": 20.0,
                "very_low_battery_percent": 10.0,
                "very_low_flash_rate": 2.0,
            }],
        )
    ])
