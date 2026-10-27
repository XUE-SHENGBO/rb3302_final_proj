# RB3302 robot navigation and landmark missions

See [the Chinese operating guide](README_zh-CN.md) for the copy-and-paste procedure for robot `ubuntu@192.168.50.6`, project `~/rb3302_xue/rb3302_final_proj_code`, ROS 2 Jazzy, domain **6**.

Run `./start1.sh` for hardware, `./start2.sh` for localization/navigation, and `./start3.sh` for a mission. Interactive launches automatically use separate tmux sessions when available. Re-running a launcher reattaches to its session. Detaching or closing SSH does not stop the robot; use Ctrl+C in mission, navigation, then hardware order.

Set the actual pose with RViz's **2D Pose Estimate**. Enter exactly four target letters, then press Enter again after the mission reports READY. Preparation does not consume the new mission's time budget.

Implemented behavior:

- Exactly four ordered A–X targets by default, including repeated letters. `./start3.sh --practice` permits other nonempty route lengths.
- A 180-second total deadline, including travel, recoveries, retries and dwell. Individual navigation attempts default to 60 seconds, with one retry.
- At least three continuous seconds stopped at every target, including the last. Fresh odometry and map-frame position are checked; motion or invalid telemetry resets the dwell timer.
- Explicit start via terminal Enter or `/mission_manager/start` (`std_srvs/srv/Trigger`). `/mission_manager/status` reports state and remaining time.
- Coordinates loaded from `student_ws/src/competition_manager/config/landmarks.yaml`; the original measured A–X positions are preserved. Optional start-letter/compass initialization requires surveyed `map_north_yaw`.
- Goal yaw defaults to the incoming travel direction instead of always zero. The existing RViz pose is preserved.
- Nav2 XY tolerance is 0.06 m; the mission also checks an arrival radius of 0.08 m and measured stationary speeds.
- Default failure policy is stop after bounded retries. Optional `failure_policy:=skip` records skipped goals and returns a partial, non-success result.
- Atomic progress records in `~/.ros/rb3302/last_mission.json`. `./start3.sh --resume` validates the original route/landmarks and retains the original deadline, including downtime.
- Read-only deployment diagnostics: `bash scripts/check_robot.sh`. Unknown hardware aliases and system services still require correct machine provisioning.

`planning_rpp` combines A* planning and regulated pure pursuit. Initial transform waiting is 24 hours. Progress checking allows 30 seconds for 0.1 m of translation; angular acceleration limits are 3.2 rad/s². Collision checking remains enabled.

The current maze controller uses a 0.25 m lookahead (configured limits 0.15–0.4 m) and rechecks XY during final heading alignment (`goal_checker.stateful=false`). Both laser observation sources explicitly accept heights 0–2 m. Physical AMCL alpha1–alpha5 remain 0.8.

Local simulation uses `./start_sim.sh` and `./sim_mission.sh`, an independent window, domain **86**, and localhost discovery. Its ideal-odometry AMCL noise and initial covariance are generated from `simulator/config.yaml` into `simulator/log/nav2_sim_params.yaml`. That generated file must never replace the physical navigation configuration or be passed to the robot launcher. Do not transfer build/install/log directories between machines.

Before physical tests, check and synchronize the PC/robot clocks while ROS is stopped, restart hardware and navigation, set the real pose in RViz, and verify local obstacle marking plus runtime parameters. Then test a controlled 0.10 m/s single-target run before the normal four-target routes. See sections 1 and 12 of the Chinese guide for the complete commands, recording steps, expected values, and stopping procedure.

Rebuild the changed packages after sourcing ROS and the robot workspace:

```bash
cd ~/rb3302_xue/rb3302_final_proj_code/student_ws
colcon build --symlink-install --packages-select competition_manager planning_rpp
```

Configuration validation without sending a goal:

```bash
ros2 run competition_manager mission_manager --ros-args \
  -p goals:="'BCDA'" -p validate_only:=true
```

Physical validation remains necessary: map/landmark alignment, actual label coverage, footprint and sensor calibration, stationary thresholds, motor response, dynamic obstacle avoidance, and cancellation latency. Software tests do not establish competition scoring compliance. There is no camera recognition or automatic grid calibration.
