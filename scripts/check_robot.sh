#!/usr/bin/env bash
# Read-only deployment checks; never starts motors or changes device rules.
set -e
CODE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=6 ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_LOCALHOST_ONLY
source "$CODE/robot_ws/install/setup.bash"
source "$CODE/student_ws/install/setup.bash"
errors=0
for device in /dev/waverover /dev/rplidar /dev/ttyACM0; do
  if [[ -r "$device" && -w "$device" ]]; then
    echo "OK: $device 可读写"
  else
    echo "FAIL: $device 缺失或当前用户无读写权限"
    errors=$((errors+1))
  fi
done
for package in robot_init planning_rpp competition_manager nav2_simple_commander robot_localization; do
  if ros2 pkg prefix "$package" >/dev/null; then
    echo "OK: $package"
  else
    errors=$((errors+1))
  fi
done
if [[ "$(systemctl show rplidar-motor.service -p LoadState --value)" != loaded ]]; then
  echo 'FAIL: rplidar-motor.service 未安装'
  errors=$((errors+1))
fi
for action in stop restart; do
  if ! sudo -n -l /usr/bin/systemctl "$action" rplidar-motor.service >/dev/null 2>&1; then
    echo "FAIL: 当前用户缺少雷达服务的免密 $action 权限"
    errors=$((errors+1))
  fi
done
if ros2 run competition_manager mission_manager --ros-args -p goals:='"BCDA"' -p validate_only:=true; then
  echo 'OK: 任务配置和坐标文件'
else
  errors=$((errors+1))
fi
if command -v tmux >/dev/null; then
  echo 'OK: tmux 可用；可在持久会话中运行各启动脚本'
else
  echo 'INFO: 未安装 tmux；SSH 断开会中断前台任务'
fi
exit "$((errors > 0))"
