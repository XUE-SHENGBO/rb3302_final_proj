#!/usr/bin/env bash
# Opt-in experiment for odom-frame stale obstacles. Default start2 is unchanged.
set -euo pipefail
CODE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
export RB3302_NAV_PARAMS_FILE="$HOME/.ros/rb3302/candidates/local_refresh/nav2_params.yaml"
export RB3302_NAV_BT_XML="$CODE/student_ws/src/planning_rpp/config/navigate_refresh_local.xml"
python3 - "$CODE/student_ws/install/planning_rpp/share/planning_rpp/config/nav2_params.yaml" "$RB3302_NAV_PARAMS_FILE" <<'PY'
from pathlib import Path
import sys
import yaml
source, target = map(Path, sys.argv[1:])
params = yaml.safe_load(source.read_text())
params['controller_server']['ros__parameters']['FollowPath']['lookahead_dist'] = .15
local = params['local_costmap']['local_costmap']['ros__parameters']
plugins = local['plugins']
if 'static_layer' not in plugins:
    plugins.insert(0, 'static_layer')
local['static_layer'] = {
    'plugin': 'nav2_costmap_2d::StaticLayer',
    'map_subscribe_transient_local': True,
    'subscribe_to_updates': False,
}
# Higher publication rate is only for diagnostic snapshots.
local['publish_frequency'] = local.get('update_frequency', 5.0)
# Keep empty/missing scan bins from being treated as evidence of free space.
assert not local['obstacle_layer']['scan'].get('inf_is_valid', False)
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(yaml.safe_dump(params, sort_keys=False, allow_unicode=True))
print('局部刷新复测：前视0.15m；局部静态墙体+新观测；控制失败后清局部地图并等待1秒。')
print(f'候选参数：{target}')
PY
exec bash "$CODE/start2.sh"
