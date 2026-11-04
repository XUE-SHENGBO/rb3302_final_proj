#!/usr/bin/env bash
# Default: validated local static map and controller-triggered local refresh.
set -eE
# Keep output in the current terminal and report why the launcher stopped.
report_exit() {
  local status=$?
  if [[ -n "${probe_pid:-}" ]]; then
    kill -TERM "$probe_pid" 2>/dev/null || true
    wait "$probe_pid" || true
  fi
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
echo "默认导航：前视0.15m；局部静态墙体与障碍观测；控制失败后刷新局部地图并等待1秒。"
params_args=()
if [[ -n "${RB3302_NAV_PARAMS_FILE:-}" ]]; then
  [[ -f "$RB3302_NAV_PARAMS_FILE" ]] || { echo "参数文件不存在：$RB3302_NAV_PARAMS_FILE" >&2; exit 1; }
  params_args+=("params_file:=$RB3302_NAV_PARAMS_FILE")
  echo "本轮使用指定参数：$RB3302_NAV_PARAMS_FILE"
fi
if [[ -n "${RB3302_NAV_BT_XML:-}" ]]; then
  [[ -f "$RB3302_NAV_BT_XML" ]] || { echo "行为树不存在：$RB3302_NAV_BT_XML" >&2; exit 1; }
  params_args+=("bt_xml:=$RB3302_NAV_BT_XML")
  echo "本轮使用指定行为树：$RB3302_NAV_BT_XML"
fi
# Record before navigation nodes start, including transient map and static TF.
probe_log="$HOME/.ros/rb3302/nav-probe-$(date +%Y%m%d-%H%M%S).log"
mkdir -p "$(dirname "$probe_log")"
python3 "$CODE/scripts/nav_failure_probe.py" >"$probe_log" 2>&1 &
probe_pid=$!
sleep 1
if ! kill -0 "$probe_pid" 2>/dev/null; then
  echo "诊断记录器启动失败，请检查 $probe_log" >&2
  exit 1
fi
echo "导航诊断已启动：$probe_log；录包位于 ~/.ros/rb3302/nav_diagnostics/"
ros2 launch planning_rpp planning.launch.py map:="$MAP" rviz:=false "${params_args[@]}"
