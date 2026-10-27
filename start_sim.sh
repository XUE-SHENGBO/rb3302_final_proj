#!/usr/bin/env bash
set -euo pipefail
CODE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
CONFIG="$CODE/simulator/config.yaml"
HEADLESS=()
while (($#)); do
  case "$1" in
    --headless) HEADLESS=(--headless); shift ;;
    --config) CONFIG="$(realpath "$2")"; shift 2 ;;
    *) echo '用法: ./start_sim.sh [--headless] [--config 配置文件]' >&2; exit 2 ;;
  esac
done
export ROS_DOMAIN_ID=86 ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export ROS_LOG_DIR="$CODE/simulator/log/ros"
mkdir -p "$ROS_LOG_DIR"
unset ROS_LOCALHOST_ONLY ROS_STATIC_PEERS
exec 9>"${TMPDIR:-/tmp}/rb3302-simulator-domain-86.lock"
flock -n 9 || { echo '模拟器已运行，请先关闭已有实例。' >&2; exit 1; }
set +u
source /opt/ros/jazzy/setup.bash
set -u
if [[ ! -f "$CODE/simulator/install/competition_manager/share/ament_index/resource_index/packages/competition_manager" ]]; then
  echo '首次启动：构建本地导航和任务包...'
  (cd "$CODE/student_ws" && colcon --log-base "$CODE/simulator/log" build --symlink-install --build-base "$CODE/simulator/build" --install-base "$CODE/simulator/install" --packages-select planning_rpp competition_manager)
fi
set +u
source "$CODE/simulator/install/setup.bash"
set -u
SIM_PARAMS="$CODE/simulator/log/nav2_sim_params.yaml"
mapfile -t INITIAL < <(/usr/bin/python3 - "$CONFIG" "$CODE/student_ws/src/planning_rpp/config/nav2_params.yaml" "$SIM_PARAMS" <<'PY'
import sys,yaml,math
cfg=yaml.safe_load(open(sys.argv[1])); v=cfg['initial_pose']
d=yaml.safe_load(open(sys.argv[2])); a=d['amcl']['ros__parameters']
l=cfg.get('localization', {})
alpha=float(l.get('odometry_alpha', 0.01))
sigma=float(l.get('initial_position_stddev', 0.02)); yaw_sigma=float(l.get('initial_yaw_stddev', 0.03))
assert all(math.isfinite(x) and x>0 for x in (alpha,sigma,yaw_sigma))
for i in range(1,6): a[f'alpha{i}']=alpha
a.update(initial_cov_xx=sigma*sigma,initial_cov_yy=sigma*sigma,initial_cov_aa=yaw_sigma*yaw_sigma)
# Keep checking XY during final heading alignment if localization changes.
d['controller_server']['ros__parameters']['goal_checker']['stateful']=False
with open(sys.argv[3], 'w') as f: yaml.safe_dump(d,f)
for k in ('x','y','yaw'):
 x=float(v[k]); assert math.isfinite(x); print(x)
PY
)
[[ ${#INITIAL[@]} == 3 ]] || { echo '初始位姿配置无效' >&2; exit 1; }
MAP="$CODE/simulator/maps/rb3302_map.yaml"
setsid env --default-signal=INT,QUIT ros2 launch planning_rpp planning.launch.py map:="$MAP" params_file:="$SIM_PARAMS" rviz:=false set_initial_pose:=true \
 initial_pose_x:="${INITIAL[0]}" initial_pose_y:="${INITIAL[1]}" initial_pose_yaw:="${INITIAL[2]}" &
NAV_PID=$!
cleanup() {
  trap - EXIT INT TERM
  # Signal every node in the dedicated group, including from a GUI close.
  kill -INT -- "-$NAV_PID" 2>/dev/null || true
  wait "$NAV_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM
echo '模拟域: 86（仅本机）；另开终端运行 ./sim_mission.sh 输入四个目标。'
/usr/bin/python3 "$CODE/simulator/simulator.py" --config "$CONFIG" --map "$MAP" "${HEADLESS[@]}"
