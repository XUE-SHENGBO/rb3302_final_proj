#!/usr/bin/env bash
# Run from any directory. A prepared mission waits for Enter before moving.
set -e
CODE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# Reattach to the existing session instead of starting duplicate nodes.
if [[ -z "${TMUX:-}" && -t 0 ]] && command -v tmux >/dev/null 2>&1; then
  exec tmux new-session -A -s rb3302-mission bash "$CODE/start3.sh" "$@"
fi
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=6 ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_LOCALHOST_ONLY
source "$CODE/robot_ws/install/setup.bash"
source "$CODE/student_ws/install/setup.bash"
args=()
case "${1:-}" in
  --resume)
    args=(-p "resume_file:=$HOME/.ros/rb3302/last_mission.json")
    ;;
  --practice)
    read -r -p '请输入练习目标字母（例如 ROS）：' ROUTE
    ROUTE="${ROUTE^^}"
    [[ "$ROUTE" =~ ^[A-X]+$ ]] || { echo '仅允许 A-X 字母。' >&2; exit 1; }
    args=(-p "goals:=\"$ROUTE\"" -p required_goal_count:=0)
    ;;
  '')
    read -r -p '请输入四个目标字母（例如 BCDA，可重复）：' ROUTE
    ROUTE="${ROUTE^^}"
    [[ "$ROUTE" =~ ^[A-X]{4}$ ]] || { echo '必须恰好输入四个 A-X 字母。' >&2; exit 1; }
    args=(-p "goals:=\"$ROUTE\"")
    ;;
  *) echo '用法：./start3.sh [--practice|--resume]' >&2; exit 1 ;;
esac
exec ros2 run competition_manager mission_manager --ros-args "${args[@]}"
