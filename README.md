# RB3302: Deploying and Running the Robot over SSH

This guide runs the hardware drivers, localisation, navigation, and mission manager **on the robot's RUBIK Pi**, through SSH terminals. The laptop is used to copy the project and display RViz. It does not need to run the navigation servers.

The current navigation stack combines **A* global planning and Regulated Pure Pursuit (RPP) control** in `planning_rpp`. The mission manager converts an ordered string of letters A–X into map-frame goals.

**Current status:** the code supports ordered navigation, but does not yet implement the required three-second stop at every landmark or a three-minute limit for the entire mission. Read the limitations below before a graded run.

## 1. Prerequisites

- Robot powered on, with its LiDAR, IMU, and chassis connected.
- SSH access to the robot and a network connection between laptop and robot.
- ROS 2 Jazzy and `colcon` installed on the robot.
- ROS dependencies for both workspaces available on the robot, including Nav2, `nav2_simple_commander`, `robot_localization`, and Cartographer if mapping is needed.
- ROS 2 Jazzy and RViz installed on the laptop for visualisation.

Use the lab-provided hardware configuration. The checked-in configuration expects:

| Device | Configured serial port |
| --- | --- |
| Chassis | `/dev/waverover` |
| LiDAR | `/dev/rplidar` |
| IMU | `/dev/ttyACM0` |

The LiDAR launcher also expects `rplidar-motor.service` and passwordless permission for its configured `sudo -n ... systemctl` commands. These are robot-specific setup requirements; copying source code does not create device aliases, permissions, or services.

## 2. Copy the complete source project and map to the robot

Run the following **on the laptop**. Replace `YOUR_ROBOT_USER` and `YOUR_ROBOT_IP` with the actual SSH credentials. These are placeholders, not known addresses.

```bash
ROBOT=YOUR_ROBOT_USER@YOUR_ROBOT_IP
LOCAL_PROJECT=/home/lfzyzl/Project/rb3302

ssh "$ROBOT" 'mkdir -p ~/rb3302_project'

rsync -av \
  --exclude='.git/' \
  --exclude='build/' \
  --exclude='install/' \
  --exclude='log/' \
  --exclude='__pycache__/' \
  --exclude='.pytest_cache/' \
  "$LOCAL_PROJECT/rb3302_final_proj_code" \
  "$LOCAL_PROJECT/maps" \
  "$ROBOT:rb3302_project/"
```

This copies all source packages in both workspaces, this guide, and the existing maps. Build outputs are intentionally omitted: laptop binaries and absolute build paths must not be reused on the robot. The command does not delete remote files. When updating an existing deployment, stop its running nodes first and rebuild after copying.

The robot-side layout will be:

```text
~/rb3302_project/
├── maps/
│   ├── rb3302_map.yaml
│   └── rb3302_map.pgm
└── rb3302_final_proj_code/
    ├── README.md
    ├── robot_ws/src/
    └── student_ws/src/
```

The map is outside `rb3302_final_proj_code` in the laptop checkout, so it must be copied separately as shown. Both the YAML and the image referenced by it are required.

## 3. SSH into the robot and build both workspaces

From the laptop:

```bash
ssh YOUR_ROBOT_USER@YOUR_ROBOT_IP
```

Then run **on the robot**:

```bash
source /opt/ros/jazzy/setup.bash
export PROJECT_ROOT="$HOME/rb3302_project"

cd "$PROJECT_ROOT/rb3302_final_proj_code/robot_ws"
colcon build --symlink-install
source install/setup.bash

cd "$PROJECT_ROOT/rb3302_final_proj_code/student_ws"
colcon build --symlink-install
source install/setup.bash
```

Stop here if either build fails. If a dependency is missing, on a robot with `rosdep` already configured, check/install declared dependencies and build again:

```bash
cd "$PROJECT_ROOT/rb3302_final_proj_code"
rosdep install --from-paths robot_ws/src student_ws/src --ignore-src -r -y
```

Verify that the new mission executable is installed:

```bash
ros2 pkg executables competition_manager
ros2 pkg prefix planning_rpp
ros2 pkg prefix nav2_simple_commander
ros2 pkg prefix robot_localization
```

The first command should list `competition_manager mission_manager`. After changing Python code, rebuild `competition_manager` if needed; after changing installed launch/configuration files, rebuild the affected package and source the workspace again.

## 4. Set up every robot terminal

Open three SSH terminals to the robot. In **each** one, run:

```bash
source /opt/ros/jazzy/setup.bash
export PROJECT_ROOT="$HOME/rb3302_project"
export ROS_DOMAIN_ID=10
source "$PROJECT_ROOT/rb3302_final_proj_code/robot_ws/install/setup.bash"
source "$PROJECT_ROOT/rb3302_final_proj_code/student_ws/install/setup.bash"
```

Use the same `ROS_DOMAIN_ID` on the laptop. `10` matches the laptop environment observed when writing this guide; use your group's assigned value if different. Network discovery must be enabled between machines; a localhost-only ROS configuration will prevent laptop RViz from receiving robot data.

## 5. Robot terminal A: start the hardware

```bash
ros2 launch robot_init robot.launch.py
```

Keep this terminal running. It starts the chassis driver, LiDAR, IMU, robot model, and static transforms. Do not start a second copy if the same drivers are already running through another terminal or service.

In terminal B, check the data before starting navigation:

```bash
ros2 topic list
ros2 topic hz /scan
```

Press `Ctrl+C` to finish the frequency check. Also check the other inputs, one command at a time:

```bash
ros2 topic hz /imu_data_ros
ros2 topic hz /odom/raw
```

Each should receive messages continuously. Resolve missing sensor data or serial errors before proceeding.

## 6. Robot terminal B: start localisation and navigation

Use the existing map:

```bash
ros2 launch planning_rpp planning.launch.py \
  map:="$PROJECT_ROOT/maps/rb3302_map.yaml" \
  rviz:=false
```

Keep this terminal running. `rviz:=false` allows navigation to run over SSH without a robot-side graphical display. This launch starts EKF odometry, AMCL, map server, and the Nav2 servers.

Always pass the map path explicitly: the launch file's default is `~/maps/rb3302_map.yaml`, which differs from this deployment layout.

Do not simultaneously launch `planning_astar`, another `planning_rpp`, or Cartographer mapping. They can duplicate navigation nodes or compete to publish transforms. `planning_rpp` already contains the A* planner and RPP controller.

## 7. Laptop: open RViz and set the initial pose

On the **laptop**, use the local workspaces for the RViz configuration and robot model resources:

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=10
source /home/lfzyzl/Project/rb3302/rb3302_final_proj_code/robot_ws/install/setup.bash
source /home/lfzyzl/Project/rb3302/rb3302_final_proj_code/student_ws/install/setup.bash

rviz2 -d /home/lfzyzl/Project/rb3302/rb3302_final_proj_code/student_ws/src/planning_rpp/rviz/navigation.rviz
```

If these local install files do not exist, build the local workspaces using step 3 with the laptop paths. Do not launch local hardware drivers or navigation servers.

1. Place the robot in the required starting square with the required physical bearing.
2. In RViz, ensure the Fixed Frame is `map`.
3. Click **2D Pose Estimate**.
4. Click the robot's actual location on the map and drag the arrow along its actual heading.
5. Wait for localisation. Check that laser returns align with mapped walls and the displayed pose agrees with the physical robot.

Repeat this whenever the robot is relocated. Field north is not necessarily the top of the RViz window.

During practice, first send a nearby free-space goal using RViz's navigation goal tool and verify movement and stopping. Complete this check before starting the letter mission. Exit keyboard teleoperation before autonomous navigation: it continuously publishes velocity messages, including zero commands, and can interfere with Nav2.

All manual initialisation and test goals must be completed before a graded run begins. The current mission executable has no separate arm/start trigger; it can move as soon as localisation and Nav2 are ready.

## 8. Robot terminal C: execute the ordered route

For example, to visit **B → C → D → A**:

```bash
ros2 run competition_manager mission_manager \
  --ros-args \
  -p goals:="'BCDA'"
```

Replace `BCDA` with the four assigned target letters in order. **Do not prepend the starting square** unless it is also a requested target. The nested quotes force a ROS string parameter, including for routes that YAML might otherwise interpret as another type.

Repeated letters are supported:

```bash
ros2 run competition_manager mission_manager \
  --ros-args \
  -p goals:="'BABA'"
```

Expected progress messages include:

```text
Goal 1/4: ...
Goal 1 reached
...
All goals reached in order
```

If a goal is rejected, fails, or times out, the mission stops instead of skipping it. A successful Nav2 result alone does not verify scoring conditions such as covering the centre label.

## 9. Optional: build a new map

Skip this section if the saved map and measured letter positions are valid.

Keep the hardware in terminal A running, but stop navigation in terminal B. Start mapping on the robot:

```bash
ros2 launch mapping_cartographer mapping.launch.py \
  rviz:=false \
  odom_topic:=/odom/raw
```

The explicit odometry topic uses the chassis output. The mapping configuration enables odometry, whereas its default `/odom` topic is normally supplied by the EKF in the navigation launch, which is not running in this mapping procedure.

On the laptop, open the mapping view instead of the navigation view:

```bash
rviz2 -d /home/lfzyzl/Project/rb3302/rb3302_final_proj_code/student_ws/src/mapping_cartographer/rviz/mapping.rviz
```

In another prepared robot SSH terminal, drive slowly:

```bash
ros2 run waverover_base keyboard_teleop \
  --ros-args -p linear_speed:=0.15 -p angular_speed:=0.5
```

Controls: `w`/`s` move, `a`/`d` turn, Space stops, and `q` exits. Keep the keyboard terminal focused. Survey the accessible course and check the resulting map in RViz.

While mapping remains active, save under a new name to preserve the existing map:

```bash
mkdir -p "$PROJECT_ROOT/maps"
ros2 run nav2_map_server map_saver_cli \
  -f "$PROJECT_ROOT/maps/rb3302_map_new"
```

Confirm that both `rb3302_map_new.yaml` and `rb3302_map_new.pgm` exist. Exit teleoperation and stop mapping before restarting navigation with the new YAML path. **Re-measure/verify every letter coordinate before running the mission on a new map**; the map coordinate frame may have changed.

## 10. Current code limitations

| Limitation | Consequence / required follow-up |
| --- | --- |
| No three-second dwell after each goal | `mission_manager.py` sends the next goal immediately after success. Implement and verify a stationary stop of at least three seconds at every requested landmark, including the final one. Configuring `waypoint_follower` waiting alone does not fix this: the manager uses individual `goToPose()` calls. |
| Timeout is per goal | `goal_timeout_sec` defaults to 180 seconds and is reset for each goal. There is no enforced 180-second total mission deadline covering travel, recovery, and dwell. |
| No requirement for exactly four goals | Any nonempty valid letter sequence is accepted. The operator must supply the four assigned goals; add validation for graded operation. |
| Hard-coded A–X positions | `student_ws/src/competition_manager/competition_manager/mission_manager.py` contains `letter_pos_map`. It assumes a particular map and measured landmark positions. There is no camera-based letter recognition or automatic grid calibration. |
| Initialisation is manual or numeric | The manager does not accept a starting-square letter plus a compass bearing. Use RViz, or its numeric `initial_pose` parameter with `set_initial_pose:=true`. Numeric yaw is in radians in the map frame. |
| Every target uses yaw `0.0` | Final orientations are not selected to minimise turns or match course bearings. Unnecessary rotation may increase runtime. |
| Arrival is based on Nav2 success | There is no explicit centre-label coverage check or scoring-specific position tolerance configured in the goal checker. Measure stopping accuracy and tune tolerances against the real robot footprint. |
| Failure stops the remaining route | Rejected, failed, or timed-out goals stop the mission. There is no implemented competition skip/resume workflow. |
| No separate start gate or full-run timer | Starting the executable can immediately initiate navigation. Arrange pre-run initialisation with the evaluation procedure; add an explicit start mechanism if required. |
| Obstacle avoidance requires field validation | LiDAR obstacle layers and RPP collision detection are configured, but this does not establish reliable avoidance of all new/dynamic obstacles. Validate actual footprint, clearances, sensor coverage, and replanning on the course. |
| Deployment depends on robot setup | Serial aliases, device permissions, ROS dependencies, and system services are not provisioned by the source copy. SSH disconnection can also interrupt foreground processes; use persistent terminal sessions if needed. |

This guide was checked against the source and available laptop environment. Robot-side builds, sensor connectivity, physical navigation, and scoring compliance have not been verified by writing this guide.

## 11. Troubleshooting and shutdown

| Symptom | Check |
| --- | --- |
| `Package 'competition_manager' not found` | Build `student_ws` on the robot, then source its `install/setup.bash` in the same SSH terminal. |
| Map cannot be loaded | Pass the deployed absolute YAML path and confirm that its referenced PGM exists beside it. |
| No `/scan`, `/imu_data_ros`, or `/odom/raw` | Check terminal A, physical connections, serial paths, permissions, and configured services. |
| RViz sees no robot data | Match domain IDs, verify network discovery/firewall settings, and check that ROS is not restricted to localhost. |
| Mission remains waiting for Nav2/AMCL | Set the initial pose, inspect terminal B, and check `ros2 lifecycle get /amcl` and `ros2 lifecycle get /bt_navigator`. Both should be active. |
| Missing map-to-base transform | Check sensors and initial localisation, then inspect `ros2 run tf2_ros tf2_echo map base_link`. |
| Robot goes toward the wrong letter | Check the loaded map, initial pose, and `letter_pos_map`; do not assume coordinates survive remapping. |
| Serial port busy / duplicated transforms | Check for duplicate hardware, navigation, or mapping processes. |

For a routine shutdown, press `Ctrl+C` in terminal C to cancel an active mission, then terminal B to stop navigation, then terminal A to stop the hardware nodes. Close RViz afterward. During practice, if motion becomes unsafe, use the robot's available physical stop/power control immediately; cancelling a software goal is not a hardware emergency stop.
