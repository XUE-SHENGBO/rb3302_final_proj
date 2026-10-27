#!/usr/bin/env bash
set -e
CODE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# Reattach to the existing session instead of starting duplicate nodes.
if [[ -z "${TMUX:-}" && -t 0 ]] && command -v tmux >/dev/null 2>&1; then
  exec tmux new-session -A -s rb3302-navigation bash "$CODE/start2.sh" "$@"
fi
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=6 ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_LOCALHOST_ONLY
source "$CODE/robot_ws/install/setup.bash"
source "$CODE/student_ws/install/setup.bash"
MAP=""
for candidate in \
  "$HOME/rb3302_xue/maps/rb3302_map.yaml" \
  "$CODE/maps/rb3302_map.yaml" \
  "$CODE/student_ws/maps/rb3302_map.yaml" \
  "$HOME/maps/rb3302_map.yaml"; do
  if [ -f "$candidate" ]; then
    MAP="$candidate"
    break
  fi
done
if [ -z "$MAP" ]; then
  echo "未找到 rb3302_map.yaml；请先将现有地图 YAML 和 PGM 放入 ~/rb3302_xue/maps/。" >&2
  exit 1
fi
python3 -c "import pathlib, sys, yaml; p = pathlib.Path(sys.argv[1]); image = p.parent / yaml.safe_load(p.read_text())[\"image\"]; sys.exit(0 if image.is_file() else \"地图图像不存在：\" + str(image))" "$MAP"
echo "使用地图：$MAP"
for topic in /scan /imu_data_ros /odom/raw; do
  echo "等待传感器：$topic"
  if ! timeout 15s ros2 topic echo "$topic" --once --qos-reliability best_effort >/dev/null; then
    echo "$topic 未收到消息，请检查终端 A，解决后重新执行本块。" >&2
    exit 1
  fi
done
exec ros2 launch planning_rpp planning.launch.py map:="$MAP" rviz:=false
