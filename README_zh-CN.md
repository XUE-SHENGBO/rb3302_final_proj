# RB3302：机器人部署、导航与四目标任务

已确认的机器人：`ubuntu@192.168.50.6`；项目：`~/rb3302_xue/rb3302_final_proj_code`；ROS 2 Jazzy；机器人和电脑均使用 **ROS_DOMAIN_ID=6**。地图沿用 `~/rb3302_xue/maps/rb3302_map.yaml`，电脑用 RViz 设置实际起点。

当前程序支持四目标顺序导航、明确开始触发、整轮 180 秒计时、每个目标至少连续静止 3 秒、失败重试和结果恢复。硬件误差与评分效果仍须实车验证，见第 10 节。

## 1. 日常启动：无需编辑配置

在电脑打开三个终端，分别执行以下命令登录机器人，按 SSH 提示输入密码：

```bash
ssh ubuntu@192.168.50.6
```

**机器人终端 A：硬件。**

```bash
cd ~/rb3302_xue/rb3302_final_proj_code
./start1.sh
```

**机器人终端 B：定位与导航。**

```bash
cd ~/rb3302_xue/rb3302_final_proj_code
./start2.sh
```

B 会依次检查 `/scan`、`/imu_data_ros`、`/odom/raw`，每个话题最多等待 15 秒；再检查地图 YAML 及其图像并启动 `planning_rpp`。初始 `map → base_link` 变换最多等待 **24 小时**，不必赶在一分钟内设置起点。该时限只用于准备阶段。

脚本按以下顺序寻找 `rb3302_map.yaml`，并打印实际使用的路径：`~/rb3302_xue/maps/`、源码目录的 `maps/`、`student_ws/maps/`、`~/maps/`。请确保选中的是对应实测字母坐标的地图。

**电脑终端 D：打开 RViz。** 此终端不 SSH。

```bash
bash -c '
set -e
CODE=/home/lfzyzl/Project/rb3302/rb3302_final_proj_code
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=6 ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_LOCALHOST_ONLY
source "$CODE/robot_ws/install/setup.bash"
source "$CODE/student_ws/install/setup.bash"
exec rviz2 -d "$CODE/student_ws/src/planning_rpp/rviz/navigation.rviz"
'
```

地图由机器人上的地图服务器发布，RViz 已配置订阅 `/map`，Fixed Frame 为 `map`。点击 **2D Pose Estimate**，在机器人实际位置按下鼠标，沿实际朝向拖出箭头。确认激光与墙体重合，位置和朝向正确。

**机器人终端 C：准备四目标任务。**

```bash
cd ~/rb3302_xue/rb3302_final_proj_code
./start3.sh
```

1. 输入恰好四个 A–X 目标字母，例如 `BCDA` 或 `BABA`，按回车。不要额外添加起始格。
2. 程序等待 Nav2、AMCL、有效坐标变换和静止里程计；默认保留 RViz 初始化，不会重置到原点。
3. 出现 `READY: press Enter to START` 后，**再按一次回车**才开始运动和整轮计时。
4. 每个目标在 Nav2 成功后，还需确认位置误差不超过 8 厘米、传感器数据新鲜，并连续静止至少 3 秒；最后一个目标也执行此检查。
5. 整轮计时包含行驶、Nav2 恢复、应用层重试与停留。超时发送取消和零速度，停止后续目标。

成功结束输出 `All goals reached in order` 和耗时。结果保存在机器人 `~/.ros/rb3302/last_mission.json`，包含每个目标的完成、失败、跳过状态。

### SSH 断线与关闭

本机已安装 `tmux`。三个脚本在交互终端中自动使用独立持久会话：`rb3302-hardware`、`rb3302-navigation`、`rb3302-mission`。再次执行对应脚本会回到原会话，不会重复启动节点。按 **Ctrl+B，再按 D** 可离开会话，后台任务继续运行；SSH 断线也不会主动停止任务。

正常停止按 **C → B → A** 顺序，在对应会话内按 `Ctrl+C`。单纯关闭 SSH 窗口不等于停车。未使用 tmux 时，程序收到终端挂断或终止信号会尝试取消任务。软件取消需要 ROS 节点和底盘仍能通信，危险运动时使用实物急停或电源控制。

## 2. 练习、跳点与恢复

三目标或单目标练习可使用：

```bash
cd ~/rb3302_xue/rb3302_final_proj_code
./start3.sh --practice
```

练习模式只放宽目标数量，其余默认仍为 180 秒总限时和至少 3 秒停留。

默认单次导航最多 60 秒，每点最多重试一次。重试不会重置整轮计时；无法确认旧目标已取消时，禁止发送下一目标。失败后默认终止任务。需要允许跳过失败目标时，可在已加载环境的机器人终端执行：

```bash
ros2 run competition_manager mission_manager --ros-args \
  -p goals:="'BCDA'" -p failure_policy:=skip
```

跳点会记录 `skipped`，最终结果为 `partial` 且退出码非零，不会伪报全部完成。

显式恢复上一轮：

```bash
cd ~/rb3302_xue/rb3302_final_proj_code
./start3.sh --resume
```

恢复只跳过已完整完成或明确跳过的访问；中断在停留过程中时，该次访问仍需重新确认和停留。恢复会校验路线、坐标文件和总限时，**暂停、断线和重新准备的墙钟时间也计入原轮 180 秒**。已超时的记录不能获得新的时间额度；开始新一轮请使用普通 `./start3.sh`。恢复任意目标数量的练习记录时，应直接运行节点并传入 `required_goal_count:=0` 与 `resume_file`。

非交互环境可通过服务开始，并查看状态：

```bash
ros2 service call /mission_manager/start std_srvs/srv/Trigger '{}'
ros2 service call /mission_manager/status std_srvs/srv/Trigger '{}'
```

开始服务只在 `READY` 阶段接受请求，提前发送不会排队触发未来运动。节点默认不自动开始；测试程序可显式设置 `start_automatically:=true`。

## 3. 更新源码与编译

更新时先停止正在执行的任务。以下在机器人上执行：

```bash
bash -c '
set -e
CODE="$HOME/rb3302_xue/rb3302_final_proj_code"
source /opt/ros/jazzy/setup.bash
cd "$CODE/robot_ws"
colcon build --symlink-install
source install/setup.bash
cd "$CODE/student_ws"
colcon build --symlink-install
source install/setup.bash
'
```

本轮只修改任务与导航配置时，可以只重编译：

```bash
bash -c '
set -e
source /opt/ros/jazzy/setup.bash
source "$HOME/rb3302_xue/rb3302_final_proj_code/robot_ws/install/setup.bash"
cd "$HOME/rb3302_xue/rb3302_final_proj_code/student_ws"
colcon build --symlink-install --packages-select competition_manager planning_rpp
'
```

任务代码在下次启动 `start3.sh` 时加载。导航 YAML 的持久配置通常需要重启终端 B 才会加载；已在线更新的参数会立即生效。重新启动导航后需要重新确认定位。

首次复制使用电脑端命令；不复制跨机器编译产物，不删除机器人现有文件：

```bash
rsync -av \
  --exclude='.git/' --exclude='build/' --exclude='install/' --exclude='log/' \
  --exclude='__pycache__/' --exclude='.pytest_cache/' \
  /home/lfzyzl/Project/rb3302/rb3302_final_proj_code \
  /home/lfzyzl/Project/rb3302/maps \
  ubuntu@192.168.50.6:rb3302_xue/
```

## 4. 部署检查

在机器人执行只读检查，不会启动电机：

```bash
cd ~/rb3302_xue/rb3302_final_proj_code
bash scripts/check_robot.sh
```

检查 ROS 包、任务配置、`/dev/waverover`、`/dev/rplidar`、`/dev/ttyACM0` 的访问权限，以及 `rplidar-motor.service` 和所需免密服务控制权限。源码无法猜测未知硬件的 USB 标识；换机器人时仍须按实验室硬件配置建立串口别名和服务。

依赖缺失且已配置 rosdep 时：

```bash
cd ~/rb3302_xue/rb3302_final_proj_code
rosdep install --from-paths robot_ws/src student_ws/src --ignore-src -r -y
```

## 5. 地图与字母坐标

字母位置已从 Python 源码移到：

```text
student_ws/src/competition_manager/config/landmarks.yaml
```

文件包含 `map_frame`、A–X 的 `[x, y]` 和可选 `map_north_yaw`。默认使用原有实测坐标，不需要额外修改。参数 `landmarks_file` 可指向另一份测量文件；加载时检查完整字母集合、坐标有限性及坐标系名称。地图改动后仍须重测或核对坐标；目前没有摄像头识别或自动标定功能。

默认目标朝向由“当前位置 → 目标点”的方向决定，避免每点都强行转向地图正 X 轴。重复或极近目标保留当前朝向。需要固定朝向时设置 `goal_heading_mode:=fixed` 和 `fixed_goal_yaw`（弧度）。

## 6. 可选：按起始格和罗盘方向初始化

日常仍推荐 RViz。也支持 `initial_letter` 与 `initial_heading`（`N/E/S/W`）。使用前必须先测量场地北向在地图坐标系内的 yaw，写入 `landmarks.yaml` 的 `map_north_yaw`；默认 `null` 会拒绝此方式，避免猜错朝向。

完成北向标定后，例如从 A 格面向北开始：

```bash
ros2 run competition_manager mission_manager --ros-args \
  -p goals:="'BCDA'" -p initial_letter:=A -p initial_heading:=N
```

也可使用数值 `initial_pose:=[x,y,yaw]` 并显式设置 `set_initial_pose:=true`。数值初始化与字母初始化不能同时启用。

## 7. 可选：重新建图

保持 A 中的硬件运行，停止任务和导航，在已加载工作空间环境的机器人终端执行：

```bash
ros2 launch mapping_cartographer mapping.launch.py rviz:=false odom_topic:=/odom/raw
```

电脑打开建图显示配置：

```bash
rviz2 -d /home/lfzyzl/Project/rb3302/rb3302_final_proj_code/student_ws/src/mapping_cartographer/rviz/mapping.rviz
```

机器人另一个已加载环境的终端低速遥控：

```bash
ros2 run waverover_base keyboard_teleop --ros-args -p linear_speed:=0.15 -p angular_speed:=0.5
```

`w/s` 前后、`a/d` 转向、空格停车、`q` 退出。保存新地图时保持建图运行：

```bash
mkdir -p ~/rb3302_xue/maps
ros2 run nav2_map_server map_saver_cli -f ~/rb3302_xue/maps/rb3302_map_new
```

确认 YAML 及其引用图像存在。退出遥控、停止建图后再启动导航；不要同时运行 Cartographer 与 AMCL 导航。使用新地图前核对 A–X 坐标；默认启动脚本不会自动切换到新地图文件名。

## 8. 默认任务参数

| 参数 | 默认值 | 含义 |
| --- | --- | --- |
| `required_goal_count` | `4` | 四目标；`0` 表示任意非空合法路线 |
| `mission_timeout_sec` | `180.0` | 从明确开始触发起的整轮预算 |
| `goal_timeout_sec` | `60.0` | 每次导航尝试上限；也受整轮预算约束 |
| `dwell_sec` | `3.0` | 连续静止停留，禁止设为小于 3 秒 |
| `arrival_timeout_sec` | `15.0` | Nav2 成功后验证到点并停稳的上限 |
| `arrival_tolerance` | `0.08` | 任务层位置误差上限（米） |
| `stopped_linear_tolerance` | `0.02` | 视为静止的平移速度上限（米/秒） |
| `stopped_angular_tolerance` | `0.05` | 视为静止的角速度上限（弧度/秒） |
| `telemetry_timeout_sec` | `0.5` | 里程计接收最大间隔 |
| `tf_timeout_sec` | `1.0` | 坐标变换最大滞后 |
| `max_retries` | `1` | 每点初次失败后的额外尝试次数 |
| `failure_policy` | `stop` | 可选 `skip`，跳过不会计为完成 |
| `start_automatically` | `false` | 默认必须回车或服务明确开始 |
| `validate_only` | `false` | 为 true 时只验证配置，不发送目标 |

Nav2 的位置容差为 6 厘米、朝向容差为 0.20 弧度；任务层再检查位置和静止状态。当前进展检查为 30 秒内平移至少 0.1 米，RPP 与速度平滑器角加速度上限为 3.2 rad/s²。最高平移速度仍为 RPP 的 0.3 米/秒，碰撞检测保持启用。

## 9. 故障排查

| 现象 | 检查与处理 |
| --- | --- |
| 导航一直等待 | 检查 A 中传感器；在 RViz 设置起点；查询 `/amcl`、`/bt_navigator` 生命周期是否为 `active` |
| `READY` 后没有运动 | 按回车或调用开始服务；这是准备状态，不计时 |
| 任务启动后位置跳到原点 | 确认已部署新版 `competition_manager`，默认保留 RViz 定位 |
| `Failed to make progress` 或转向缓慢 | 对比 `/cmd_vel_nav_raw`、`/cmd_vel`、`/odom`；检查定位和实际转向，避免只提高最高速度 |
| Nav2 成功但停留检查失败 | 查看实际位置、里程计是否持续更新及小车是否仍在移动；退出遥控和其他速度发布程序 |
| RViz 没地图 | 检查 `/map`、两端域编号 `6`、网络发现；Map 显示的 Durability 设为 Transient Local |
| 找不到包或配置 | 编译两个工作空间，并在当前终端加载 `install/setup.bash` |
| 恢复失败 | 检查路线、坐标文件是否变动，以及原轮 180 秒是否已用完 |
| 无法同时开第二个任务 | 同一用户、同一 ROS 域只允许一个任务管理器；先停止旧任务 |

每个普通 SSH 终端需要 ROS 环境时，复制：

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=6 ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_LOCALHOST_ONLY
source ~/rb3302_xue/rb3302_final_proj_code/robot_ws/install/setup.bash
source ~/rb3302_xue/rb3302_final_proj_code/student_ws/install/setup.bash
```

## 10. 原局限的处理状态与实车验收

| 原局限 | 当前处理 |
| --- | --- |
| 每点没有停留 3 秒 | 已实现连续静止计时，包含最后一点；移动、数据过期或偏离目标会重新计时 |
| 只有单点超时 | 已实现整轮 180 秒预算，覆盖导航、恢复、重试和停留；超时取消并发送零速度 |
| 不强制四个目标 | 默认恰好四个；练习模式可显式放宽，重复字母按独立访问处理 |
| 字母坐标写死 | 已移至可替换 YAML，启动校验；地图变化后仍须重新测量 |
| 起点只能手动/数值设置 | 已增加起始格 + 罗盘朝向；需要先标定地图北向，默认仍用 RViz |
| 所有目标 yaw 为 0 | 默认按入站方向选择目标朝向，也支持固定朝向 |
| 到达只看 Nav2 结果 | 增加任务层位置检查、实测速度检查和连续停留；Nav2 配置明确位置容差 |
| 失败后没有继续方式 | 有限重试、显式跳点和检查点恢复；已用时间不因恢复清零 |
| 没有独立开始触发 | READY 后回车或服务开始；准备时间不计入新一轮 |
| SSH 断开会中断任务 | 三个启动脚本自动使用本机 tmux 持久会话，支持重新连接 |
| 部署依赖机器配置 | 增加只读部署检查；未知设备别名和系统服务仍需实验室提供正确配置 |

以下项目**仍须随后实车验收**，不能仅凭代码或软件测试认定通过：

- A–X 测量坐标是否与当前地图、实物中心标签对应；地图北向是否已标定。
- 6–8 厘米软件容差是否足以让实际车体覆盖中心标签。当前检查使用 `base_link` 参考点，不是摄像头或标签覆盖检测；须结合实物轮廓、定位误差及标签尺寸调整。
- 每点是否实际连续静止至少 3 秒，以及整轮是否在 180 秒内完成；当前速度阈值需结合传感器噪声验证。
- 转向加速度调整后的起转、停车与狭窄处通行表现；车体 footprint、传感器外参和电机响应是否准确。
- 对新增或动态障碍物的避让、重新规划及恢复效果；现有激光障碍层和碰撞预测需在场地验证。
- 超时或中断时的取消与停车延迟。软件发送取消/零速度不等于硬件实时急停，通信或驱动故障仍需实物停止手段。

本轮代码验收包括离线任务规则测试及隔离 ROS 域内的模拟动作测试；最终实车结果在完成上述测试后记录。程序没有摄像头字母识别或自动网格标定功能，这些功能不能通过修改现有坐标导航逻辑替代。
