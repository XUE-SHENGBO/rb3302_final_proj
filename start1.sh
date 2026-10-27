#!/usr/bin/env bash
set -e
CODE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# Reattach to the existing session instead of starting duplicate nodes.
if [[ -z "${TMUX:-}" && -t 0 ]] && command -v tmux >/dev/null 2>&1; then
  exec tmux new-session -A -s rb3302-hardware bash "$CODE/start1.sh" "$@"
fi
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=6 ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_LOCALHOST_ONLY
source "$CODE/robot_ws/install/setup.bash"
source "$CODE/student_ws/install/setup.bash"
exec ros2 launch robot_init robot.launch.py
