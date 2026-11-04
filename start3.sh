#!/usr/bin/env bash
# Run from any directory. A prepared mission waits for Enter before moving.
set -eE
# Keep output in the current terminal and report why the launcher stopped.
report_exit() {
  local status=$?
  local reason
  case "$status" in
    0) reason="正常结束" ;;
    129) reason="终端挂断（SIGHUP）" ;;
    130) reason="用户中断（Ctrl+C / SIGINT）" ;;
    137) reason="进程被强制终止（SIGKILL），请检查系统日志" ;;
    143) reason="收到终止信号（SIGTERM）" ;;
    *) reason="执行失败，请查看上方报错" ;;
  esac
  printf '\n[%s] %s；退出码：%s\n' "${BASH_SOURCE[0]##*/}" "$reason" "$status" >&2
}
trap report_exit EXIT
trap 'printf "\n[%s] 命令失败（退出码 %s），%s:%s\n  %s\n" "${0##*/}" "$?" "${BASH_SOURCE[0]}" "$LINENO" "$BASH_COMMAND" >&2' ERR
CODE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
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
ros2 run competition_manager mission_manager --ros-args "${args[@]}"
