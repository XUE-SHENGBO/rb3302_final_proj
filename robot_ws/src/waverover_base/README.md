# WAVE ROVER measured feedback and diagnostics

The driver publishes odometry only from newly received, complete, finite T=1001
packets. Host monotonic receive intervals are used for velocity; the firmware
protocol currently has no verified sampling timestamp. ROS header stamps retain
the receive time. Cached timer ticks and T=1002 packets do not refresh odometry.

`/waverover/driver_diagnostics` (JSON String) and `/diagnostics` report sample age,
invalid/rebased packets, queue drops, selected distance source, both centre and
wheel-mean velocities, their distance residual, and the motion gate state.
`/waverover/json_feedback` now contains received packets, without timer duplicates.
Record it together with `/cmd_vel`, `/cmd_vel_nav_raw`, `/cmd_vel_smoothed`,
`/odom/raw`, `/odom`, `/imu_data_ros`, `/scan`, `/tf`, `/tf_static`, `/amcl_pose`,
`/plan`, both costmaps and `/lookahead_collision_arc` for ground calibration.

## Defaults and validity

| Parameter | Default | Meaning |
|---|---|---|
| `odom_distance_source` | `firmware_centre` | Retains previous source. `wheel_mean` is opt-in after scale/sign verification. |
| `yaw_odom_unit` | `radians` | Explicit `radians` or `degrees`; never inferred from magnitude. |
| `wheel_yaw_rate_enabled` | false | Uncalibrated wheel yaw rate is diagnostic-only. |
| `wheel_track_width` | 0.125 m | Nominal, not a ground-slip calibration. |
| `feedback_timeout_sec` | 0.5 s | Invalid/stale feedback inhibits motion. |
| `feedback_max_gap_sec` | 0.5 s | Longer intervals establish a new baseline. |
| `max_feedback_wheel_speed` | 1.5 m/s | Reject implausible wheel/centre increments; tune from physical limits. |
| `max_feedback_yaw_rate` | 12 rad/s | Reject implausible firmware-yaw jumps. |
| `feedback_sequence_field` | empty | Enable only if the actual firmware provides a verified increasing integer field. |
| `odom_linear_variance` | 0.0025 (m/s)^2 | Provisional stddev 0.05 m/s, not measured accuracy. |
| `odom_wheel_yaw_rate_variance` | 0.04 (rad/s)^2 | Used only when wheel yaw rate is explicitly enabled. |
| `firmware_main_type` / `firmware_module_type` | 1 / 0 | Existing initialization preserved; verify physical hardware before changing. |

When wheel yaw rate is disabled, angular.z=0 is an unavailable-value placeholder,
with variance 1e6 and `yaw_rate_valid=false` in diagnostics. It is not a measured
stationary angular velocity. Current navigation EKF must continue to fuse only
raw linear.x and use the independent IMU for yaw/yaw rate. Raw pose and unused
twist components also carry variance 1e6. Do not enable new fusion components
without independent calibration. Raw odometry TF remains disabled by default.

Repeated equal values in *separately received* stationary packets are valid. A
configured firmware sequence detects retransmission/restart. With no such field,
the driver cannot distinguish a repeated hardware packet from a new equal sample.
Counter resets, impossible increments, nonpositive intervals, long gaps and ROS
clock jumps invalidate/rebaseline feedback; no increment is integrated across a
detected discontinuity. There is no verified device reboot identifier, so small
resets that do not reset both encoder counts to zero may still require protocol
support to detect reliably.

The old `dist_centre` source remains active, while the wheel-mean alternative and
residual are observable. This version does **not** claim to fix firmware centre
distance semantics, motor deadzone, effective track width, or physical slip.
Do not treat diagnostic-only wheel yaw as measured body motion.

## Motion and device ownership

Feedback loss/invalidity or command timeout produces zero velocity. Recovery does
not replay a cached command; a new valid command is required. Invalid numerical
commands also stop. The firmware heartbeat remains a fallback; software cannot
guarantee a stop if the serial link or motor controller is broken.

A process lock canonicalizes device symlinks and is acquired before service
management. The serial port uses POSIX exclusive locking, and a /proc FD check
detects accessible legacy owners. /proc visibility restrictions and noncooperating
future writers cannot be eliminated by advisory locks. Initialization refuses an
already open device. Only a service stopped by this instance is restarted; device
ownership is released after cleanup. Partial serial lines are buffered without
blocking speed/stop writes for the old one-second read timeout.

## Validation without moving a robot

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=219 ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
export ROS_LOG_DIR=/tmp/rb3302-driver-tests
export PYTHONPATH="$PWD/robot_ws/src/waverover_base:$PYTHONPATH"
python3 -m pytest -q robot_ws/src/waverover_base/test
```

Unit tests cover packet faults, clock/gap/reset handling, both distance sources,
angle units, command recovery and cross-process ownership. ROS tests use a PTY
and replace service control; they never open the robot serial device. They check
actual JSON wire commands, odometry/covariances, stale-feedback stops, partial
lines, second-instance refusal and initialization cleanup.

Offline historical audit, without creating a ROS node or opening serial:

```bash
ros2 run waverover_base replay_feedback /absolute/path/to/bag \
  --start 1793605549.72835 --duration 17 --output /tmp/feedback-comparison.json
```

Old bags may contain timer-republished cached packets and use host topic arrival
times. Replay compares semantics but cannot validate physical calibration.

## Ground calibration and rollout

First verify firmware/version/model, wheel direction, wheel scale and command
units. Separate bench wheel checks from ground turning: effective track width
under skid must be measured on the floor. Compare command → wheel feedback → IMU
and independent/scan rotation, in both directions and through reversals. Diagnose
deadzone, delay and slip separately; do not multiply all angular commands by an
unverified constant. Only then select the distance source or implement a bounded
body-angular-rate loop at the base layer. Keep map/AMCL/RPP unchanged for this
comparison, then retest F→L and X→V with recorded costmaps.

Build/deploy while navigation is stopped, retain the Git pre-change commit, and
restart driver/EKF/localization together at a stationary, verified pose. Never
switch cumulative-distance baselines during motion. Restore the complete previous
package and rebuild to roll back. Installation alone does not replace a running
process; a restart is needed to load the new driver.
