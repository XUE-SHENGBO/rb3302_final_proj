from launch import LaunchDescription
from launch.actions import ExecuteProcess


SERVICE = "rplidar-motor.service"
PORT = "/dev/rplidar"


def generate_launch_description():

    rplidar_with_motor_guard = ExecuteProcess(
        cmd=[
            "bash",
            "-lc",
            f'''
            set -e

            cleanup() {{
                echo "[rplidar_launch] Restarting {SERVICE}..."
                sudo -n /usr/bin/systemctl restart {SERVICE}
            }}

            trap cleanup EXIT INT TERM

            echo "[rplidar_launch] Stopping {SERVICE}..."
            sudo -n /usr/bin/systemctl stop {SERVICE}

            sleep 1.5

            echo "[rplidar_launch] Starting rplidar_node..."
            ros2 run rplidar_ros rplidar_node --ros-args \
                -r __node:=rplidar_node \
                -p serial_port:={PORT} \
                -p serial_baudrate:=115200 \
                -p frame_id:=laser \
                -p angle_compensate:=true \
                -p scan_mode:=Standard
            '''
        ],
        output="screen",
    )

    return LaunchDescription([
        rplidar_with_motor_guard,
    ])