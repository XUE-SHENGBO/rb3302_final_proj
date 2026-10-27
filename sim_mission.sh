#!/usr/bin/env bash
set -euo pipefail
CODE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
export ROS_DOMAIN_ID=86 ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export ROS_LOG_DIR="$CODE/simulator/log/ros"
mkdir -p "$ROS_LOG_DIR"
unset ROS_LOCALHOST_ONLY ROS_STATIC_PEERS
set +u
source /opt/ros/jazzy/setup.bash
source "$CODE/simulator/install/setup.bash"
set -u
read -r -p '请输入四个目标字母（A-X，例如 CJKL）：' ROUTE
ROUTE="${ROUTE^^}"
[[ "$ROUTE" =~ ^[A-X]{4}$ ]] || { echo '必须恰好输入四个 A-X 字母。' >&2; exit 1; }
exec ros2 run competition_manager mission_manager --ros-args -p "goals:=\"$ROUTE\"" -p "result_file:=$HOME/.ros/rb3302/sim_last_mission.json"
