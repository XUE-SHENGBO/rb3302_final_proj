# KNHX planning recovery

## Wall-end turning clearance

`turn_clearance.py` rebuilds inflation from recorded global lethal/unknown cells using the installed native Nav2 planner. It compares baseline/candidate K plans, samples the candidate local rectangular footprint at 1 cm path intervals and 5° yaw intervals, and checks that the wider global planning envelope preserves previously reachable landmarks. A rotation sweep is stronger than checking a centerline but still a discrete grid check, not a sensor or hardware guarantee.

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=217 ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
python3 scripts/nav_recovery_test/turn_clearance.py \
  --baseline /path/to/actual-loaded-before.yaml \
  --candidate student_ws/src/planning_rpp/config/nav2_params.yaml \
  --case /path/to/test1.db3 1793784891.7735 \
  --case /path/to/test2.db3 1793784975.9894 \
  --landmarks student_ws/src/competition_manager/config/landmarks.yaml \
  --output /tmp/turn-clearance-regression
```

Only `ComputePathToPose` actions are used; no controller or motion goal is started. The physical robot must load the deployed YAML through a new `start2.sh` session. Existing navigation processes keep their previous settings. Global padding 0.13 m is a planning envelope; local padding remains 0.01 m with the original rectangular body. Cost-based RPP speed scaling remains disabled in this clearance-only change.

2026-11-04 validation: both recorded starting grids produced 41 unsafe baseline rotation-sweep samples and zero candidate unsafe samples. All 24 measured letters remained reachable on both grids. The real Nav2 controller with the maze simulator completed K from the recorded first start in 15.54 seconds, on attempt 1, including the three-second stop; no collision alarm or sampled body contact occurred. Simulation used an explicit known-pose AMCL initialization with small covariance; an earlier launch-only initialization failed the unchanged readiness gate before motion. These results validate planning geometry and an ideal closed-loop turn, not physical scan coverage or the full competition route. The deployed baseline AMCL `update_min_a=0.1`, RPP `max_angular_accel=5.0`, local radius 0.55 m and local scaling 5.0 are preserved; unrelated recorder edits are not part of this fix.

KNHX failed at its first goal K: NavFn returned NO_VALID_PATH (208) immediately, and six mission attempts ended in about 0.25 seconds. Recorded global maps showed an observation-layer obstacle at K while the saved static map was free. This does not establish which scan originally created the mark.

The default `navigate_refresh_local.xml` now wraps planning in its own bounded recovery. Recoverable planner errors clear the global costmap, wait one second for updates, then replan, up to two recoveries. The existing controller/local recovery remains. Nav2 StaticLayer is not clearable; live finite scans still mark obstacles. `inf_is_valid` remains unchanged because the RPLIDAR driver also represents invalid zero-distance readings as infinity. The mission layer waits stopped for `retry_delay_sec=1.0` between failures, with normal deadline and shutdown processing. Exhausted retries still stop the mission.

Tests below use actual installed ROS 2 Jazzy/Nav2 libraries, synthetic scans and synthetic action servers. They never use robot domain 6. Run them sequentially:

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=217 ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
cmake -S scripts/nav_recovery_test -B /tmp/rb3302-knhx-bt-build
cmake --build /tmp/rb3302-knhx-bt-build -j2
/tmp/rb3302-knhx-bt-build/check "$PWD/student_ws/src/planning_rpp/config/navigate_refresh_local.xml"
python3 scripts/nav_recovery_test/global_costmap.py
python3 -m pytest -q student_ws/src/competition_manager/test/test_mission_logic.py student_ws/src/competition_manager/test/test_velocity_guard.py
RB3302_ROS_INTEGRATION=1 python3 -m pytest -q student_ws/src/competition_manager/test/test_ros_mission_integration.py
```

The native BT test verifies planner error -> global clear -> one-second wait -> successful replan; persistent planning failure stops after three planning calls; invalid planner configuration does not clear maps; controller/local recovery still works. The real planner test reproduces 208 from a retained observation, verifies successful planning after refresh, checks static wall preservation and confirms new/persistent finite observations still block the map. These regressions do not certify the physical KNHX route.

Deployment: save the robot's current source files first, copy the committed files, then rebuild `competition_manager` and `planning_rpp` in `student_ws`. Verify installed XML/Python hashes against source. Restart navigation with `./start2.sh` and create a new mission with `./start3.sh` to use the complete change. Syncing/building alone does not replace already running Python processes or guarantee a running navigator reloads its cached behavior tree. Do not auto-start navigation as part of deployment.

The pre-fix source snapshot is commit `8930465` on branch `codex/knhx-planner-recovery-20261104`. To roll back these changes, restore `start2.sh`, both README files, the mission manager and its test, and the behavior tree from that commit, then rebuild both packages and restart navigation. Do not reset unrelated robot changes.

## Stationary AMCL verification

`localization_guard.py` adds a bounded preparation/recovery gate using current AMCL uncertainty, finite scan matching to saved walls, and consecutive pose stability. It never resets the initial pose, calls global localization, or publishes nonzero velocity. Existing motion/goal tests now supply synthetic AMCL/map/scan data; the recovery integration case deliberately degrades covariance after a failed navigation action and verifies stationary updates followed by global/local refresh before a second goal.

For the recorded KNHX session, freeze its stationary scans and odometry before the first command, then run actual AMCL and the production gate:

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=217 ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
python3 scripts/nav_recovery_test/amcl_replay.py /path/to/20261104-080115/bag/bag_0.db3 --output /tmp/amcl-replay.json
python3 scripts/nav_recovery_test/amcl_replay.py /path/to/20261104-080115/bag/bag_0.db3 --hold-ready-seconds 8 --output /tmp/amcl-ready-wait.json
python3 -m pytest -q student_ws/src/competition_manager/test/test_localization_guard.py
RB3302_ROS_INTEGRATION=1 python3 -m pytest -q student_ws/src/competition_manager/test/test_ros_mission_integration.py
```

The replay intentionally uses a frozen physical pose and repeated real stationary frames, not a closed-loop robot trajectory. It verifies refinement of a broad initial particle distribution, not the physical KNHX route or every ambiguous map position. An unchanged or incorrectly initialized pose can still fail the bounded gate; the operator must then set the measured pose. Package runtime dependencies remain unchanged.

The hold-ready case tests actual AMCL's stationary publication behavior beyond the two-second pose-age limit, then triggers START without sending a navigation goal. No synthetic costmap services are started: an unexpected full recovery/map clear during healthy waiting therefore fails this regression. It covers manual preparation waiting rather than only automatic-start paths.
