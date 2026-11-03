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
mission_limit=600.0
goal_limit=180.0
case "${1:-}" in
  --resume)
    args=(-p "resume_file:=$HOME/.ros/rb3302/last_mission.json")
    mission_limit=$(python3 -c 'import json,sys; print(float(json.load(open(sys.argv[1]))["mission_timeout_sec"]))' "$HOME/.ros/rb3302/last_mission.json")
    [[ "$mission_limit" != 180.0 && "$mission_limit" != 180 ]] || goal_limit=60.0
    ;;
  --practice)
    read -r -p '请输入练习目标字母（例如 ROS）：' ROUTE
    ROUTE="${ROUTE^^}"
    [[ "$ROUTE" =~ ^[A-X]+$ ]] || { echo '仅允许 A-X 字母。' >&2; exit 1; }
    args=(-p "goals:=\"$ROUTE\"" -p required_goal_count:=0)
    ;;
  ''|--competition)
    if [[ "${1:-}" == --competition ]]; then
      mission_limit=600.0
      goal_limit=180.0
    fi
    read -r -p '请输入四个目标字母（例如 BCDA，可重复）：' ROUTE
    ROUTE="${ROUTE^^}"
    [[ "$ROUTE" =~ ^[A-X]{4}$ ]] || { echo '必须恰好输入四个 A-X 字母。' >&2; exit 1; }
    args=(-p "goals:=\"$ROUTE\"")
    ;;
  *) echo '用法：./start3.sh [--practice|--competition|--resume]' >&2; exit 1 ;;
esac
echo "本轮总时限 ${mission_limit} 秒；单次导航 ${goal_limit} 秒；READY 后明确开始才计时。"
args+=(-p "mission_timeout_sec:=$mission_limit" -p "goal_timeout_sec:=$goal_limit")
exec ros2 run competition_manager mission_manager --ros-args "${args[@]}"
