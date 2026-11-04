# KNHX planning recovery

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
