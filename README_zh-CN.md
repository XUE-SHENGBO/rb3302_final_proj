# RB3302：机器人部署、导航与四目标任务

已确认的机器人：`ubuntu@192.168.50.6`；项目：`~/rb3302_xue/rb3302_final_proj_code`；ROS 2 Jazzy；机器人和电脑均使用 **ROS_DOMAIN_ID=6**。地图沿用 `~/rb3302_xue/maps/rb3302_map.yaml`，电脑用 RViz 设置实际起点。

当前程序支持四目标顺序导航、明确开始触发、整轮计时、每个目标至少连续静止 3 秒、失败重试和结果恢复。日常测试默认整轮 600 秒，比赛模式为 180 秒。硬件误差与评分效果仍须实车验证，见第 10 节。

## 1. 日常启动：无需编辑配置

实车使用域 **6** 和 `student_ws/src/planning_rpp/config/nav2_params.yaml`。模拟使用域 **86**；`simulator/config.yaml` 的初始位姿与定位噪声、`simulator/log/nav2_sim_params.yaml` 的生成参数仅供模拟。实车执行 `start1.sh` / `start2.sh` / `start3.sh`，本地模拟执行 `start_sim.sh` / `sim_mission.sh`，不要交叉使用启动脚本或参数文件。

### 启动前核对时钟

机器人曾出现 NTP 已启用但尚未同步、时间与电脑相差接近一天的问题。先确保机器人任务、导航和硬件已按 C → B → A 停止；在**本地电脑**执行：

```bash
date -u
ssh ubuntu@192.168.50.6 'date -u; timedatectl show -p NTPSynchronized'
```

如果时间明显不同，先确认电脑时间正确；在所有 ROS 节点停止的情况下，从电脑把当前时间设置到机器人（按提示输入 sudo 密码）：

```bash
ssh -t ubuntu@192.168.50.6 "sudo date -u -s '@$(date -u +%s)'"
```

然后重复前面的 `date -u` 检查。这个操作是一次性校时，不代表 NTP 已恢复；每次重启机器人后都应重新核对，避免运行中跳变系统时间。

### 启动硬件、导航和 RViz

在电脑打开三个终端，分别执行以下命令登录机器人，按 SSH 提示输入密码；另开一个本地终端供 RViz 使用：

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

`./start2.sh` 以保存地图结合实时障碍观测导航：前视距离 0.15 m，局部地图使用静态层、障碍层和膨胀层，局部地图发布 5 Hz。可恢复的规划错误会刷新全局地图并等待 1 秒后重新规划，同一规划失败序列最多恢复两次；可恢复的控制错误仍刷新局部地图并等待 1 秒。静态墙体由地图层保留，新扫描继续标记障碍，不将无效或无回波测量直接当作空闲证据。任务层失败重试前另停车等待 `retry_delay_sec`（默认 1 秒），等待包含在原轮时限内，避免瞬间耗尽重试。诊断录包自动启动。`bash scripts/start2_local_refresh.sh` 保留为兼容入口；测试与部署说明见 `scripts/nav_recovery_test/README.md`。

转正前的启动器、参数和默认行为树备份在 `backups/start2-before-local-refresh-20261104/`。备份脚本不能直接从备份目录运行；回退时将文件恢复到原路径并重新构建 `planning_rpp`。

B 会依次检查 `/scan`、`/imu_data_ros`、`/odom/raw`，每个话题最多等待 15 秒；再检查地图 YAML 及其图像并启动 `planning_rpp`。初始 `map → base_link` 变换最多等待 **24 小时**，不必赶在一分钟内设置起点。该时限只用于准备阶段。

重新启动导航后，可在机器人终端用 `ros2 param get /amcl update_min_d` 和 `ros2 param get /amcl max_beams` 确认本轮 AMCL 参数已加载；应分别显示 `0.05` 和 `100`。只重新连接现有 tmux 会话不会重新加载参数。

脚本按以下顺序寻找 `rb3302_map.yaml`，并打印实际使用的路径：`~/rb3302_xue/maps/`、源码目录的 `maps/`、`student_ws/maps/`、`~/maps/`。请确保选中的是对应实测字母坐标的地图。

**电脑终端 D：打开 RViz。** 此终端不 SSH。

```bash
bash -c '
set -e
CODE=/media/lfzyzl/WinShare/Project/rb3302/rb3302_final_proj_code
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=6 ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_LOCALHOST_ONLY ROS_STATIC_PEERS
source "$CODE/robot_ws/install/setup.bash"
source "$CODE/student_ws/install/setup.bash"
exec rviz2 -d "$CODE/student_ws/src/planning_rpp/rviz/navigation.rviz"
'
```

地图由机器人上的地图服务器发布，RViz 已配置订阅 `/map`，Fixed Frame 为 `map`。点击 **2D Pose Estimate**，在机器人实际位置按下鼠标，沿实际朝向拖出箭头。确认激光与墙体重合，位置和朝向正确。

更新配置后的首次实测，先完成第 12 节的静态检查，再启动任务。

**机器人终端 C：准备四目标任务。**

```bash
cd ~/rb3302_xue/rb3302_final_proj_code
./start3.sh
```

1. 输入恰好四个 A–X 目标字母，例如 `BCDA` 或 `BABA`，按回车。不要额外添加起始格。
2. 程序等待 Nav2、AMCL、有效坐标变换和静止里程计；默认保留 RViz 初始化，不会重置到原点。
3. 出现 `READY: press Enter to START` 后，**再按一次回车**才开始运动和整轮计时。
4. 每个目标在 Nav2 成功后，还需确认位置误差不超过 10 厘米、传感器数据新鲜，并连续静止至少 3 秒；最后一个目标也执行此检查。
5. 整轮计时包含行驶、Nav2 恢复、应用层重试与停留。超时发送取消和零速度，停止后续目标。

成功结束输出 `All goals reached in order` 和耗时。结果保存在机器人 `~/.ros/rb3302/last_mission.json`，包含每个目标的完成、失败、跳过状态。

### SSH 断线与关闭

`start2.sh` 和 `start3.sh` 直接在当前终端运行，不再自动进入 tmux；退出后保留原始报错，并打印退出原因和退出码，命令失败时还会显示命令及行号。请保持对应 SSH 终端打开，重新执行会启动新进程，请先停止旧进程。`start1.sh` 仍自动使用 `rb3302-hardware` tmux 会话。之前已启动的导航、任务 tmux 会话需自行停止，新脚本不会连接或关闭旧会话。

正常停止按 **C → B → A** 顺序，在对应终端内按 `Ctrl+C`。单纯关闭 SSH 窗口不等于停车。未使用 tmux 时，程序收到终端挂断或终止信号会尝试取消任务。软件取消需要 ROS 节点和底盘仍能通信，危险运动时使用实物急停或电源控制。

## 2. 练习、跳点与恢复

三目标或单目标练习可使用：

```bash
cd ~/rb3302_xue/rb3302_final_proj_code
./start3.sh --practice
```

普通 `./start3.sh` 和 `--practice` 默认整轮 **600 秒**、单次导航 **120 秒**；练习模式额外放宽目标数量，每点仍至少连续静止 3 秒。脚本会打印本轮实际时限。需要验证 180 秒比赛预算时运行 `./start3.sh --competition`，此模式使用整轮 180 秒、单次导航 60 秒。

默认单次导航最多 120 秒，每点最多重试一次。重试不会重置整轮计时；无法确认旧目标已取消时，禁止发送下一目标。失败后默认终止任务。需要允许跳过失败目标时，可在已加载环境的机器人终端执行：

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

恢复只跳过已完整完成或明确跳过的访问；中断在停留过程中时，该次访问仍需重新确认和停留。恢复会校验路线、坐标文件和总限时，`--resume` 自动沿用记录中的总预算，**暂停、断线和重新准备的墙钟时间也计入原轮预算**。已超时的记录不能获得新的时间额度；开始新一轮请使用普通 `./start3.sh`。恢复任意目标数量的练习记录时，应直接运行节点并传入 `required_goal_count:=0` 与 `resume_file`。

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

任务代码在下次启动 `start3.sh` 时加载。导航 YAML 更新后需要退出旧终端 B 中的导航进程，再重新执行 `start2.sh`；仅重新连接 tmux 会话不会重新加载配置。重新启动导航后需要在 RViz 重新设置实际位姿。雷达扫描源的高度过滤在初始化时加载，不应只依赖在线修改参数。

实车 AMCL 的 `alpha1`–`alpha5` 保留 **0.8**；模拟专用的 **0.01** 和较小初始协方差只由 `start_sim.sh` 写入模拟运行参数。不要把生成的 `simulator/log/nav2_sim_params.yaml` 复制到实车导航配置中，也不要向实车 `start2.sh` 注入这份文件。

2026-11-02 的 A→S 实车录包经隔离域离线重放后，实车 AMCL 配置增加了 `update_min_d/a=0.05`、`max_beams=100` 及更明确的雷达似然参数；数据和比较方法见项目外层的 [`offline_amcl/report.md`](../reports/real-test-20261102/AS-20261102-0740/offline_amcl/report.md)。后续按实测调整请求，两端导航 YAML 已同步为 `xy_goal_tolerance=0.10`、两张代价地图 `inflation_radius=0.30`、`feedback=OPEN_LOOP`（本次停车修复后） 和 RPP `transform_tolerance=0.2`；任务层 `arrival_tolerance` 同步为 0.10 m。AMCL 离线结果不代表这些后续改动已经过实车验证。导航 YAML 原文件备份于 `~/rb3302_xue/backups/20261102-nav-remaining-091142/nav2_params.before.yaml`；重新启动导航并设置实际位姿后，新值才生效。

首次复制使用电脑端命令；不复制跨机器编译产物，不删除机器人现有文件：

```bash
rsync -av \
  --exclude='.git/' --exclude='.gitignore' --exclude='.vscode/' \
  --exclude='build/' --exclude='install/' --exclude='log/' \
  --exclude='__pycache__/' --exclude='.pytest_cache/' --exclude='*.before-*' \
  /media/lfzyzl/WinShare/Project/rb3302/rb3302_final_proj_code \
  /media/lfzyzl/WinShare/Project/rb3302/maps \
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
| `mission_timeout_sec` | `600.0` | 从明确开始触发起的整轮测试预算；`--competition` 为 180 秒 |
| `goal_timeout_sec` | `120.0` | 每次导航尝试上限；`--competition` 为 60 秒；也受整轮预算约束 |
| `dwell_sec` | `3.0` | 连续静止停留，禁止设为小于 3 秒 |
| `arrival_timeout_sec` | `15.0` | Nav2 成功后验证到点并停稳的上限 |
| `arrival_tolerance` | `0.10` | 任务层位置误差上限（米），与 Nav2 的 XY 容差一致 |
| `stopped_linear_tolerance` | `0.02` | 视为静止的平移速度上限（米/秒） |
| `stopped_angular_tolerance` | `0.05` | 视为静止的角速度上限（弧度/秒） |
| `telemetry_timeout_sec` | `0.5` | 里程计接收最大间隔 |
| `tf_timeout_sec` | `1.0` | 坐标变换最大滞后 |
| `max_retries` | `1` | 每点初次失败后的额外尝试次数 |
| `failure_policy` | `stop` | 可选 `skip`，跳过不会计为完成 |
| `start_automatically` | `false` | 默认必须回车或服务明确开始 |
| `validate_only` | `false` | 为 true 时只验证配置，不发送目标 |

Nav2 与任务管理器的位置容差统一为 **0.10 m**，每点（含最后一点）必须在容差内连续静止 **3 秒**；移动、定位越界或数据失效会重新计时，日志会输出 `Dwell conditions`。字母任务不要求终点朝向，因此不再为终点额外转向；路径起始方向相差超过约 45° 时仍可原地对齐。RPP 期望速度 **0.20 m/s**，固定前瞻 **0.25 m**，末段减速范围 **0.25 m**、最低接近速度 **0.05 m/s**；曲率调速半径 **0.40 m**、最低调速速度 **0.07 m/s**，原地目标转速 **0.80 rad/s**。局部、全局膨胀半径均为 **0.30 m**。

导航输出链路为 `/cmd_vel_nav_raw → velocity_smoother → /cmd_vel_smoothed → velocity_guard → /cmd_vel`；恢复动作也经过该链路。平滑器使用 **OPEN_LOOP**，AMCL/EKF 定位反馈仍保留。速度守卫将最终输出限制在请求速度以内及 ±0.20 m/s、±1.0 rad/s，零速请求和 `/cmd_vel_stop` 直接触发停车；指令超过 0.30 秒或扫描超过 0.50 秒未更新、扫描 TF 无效时停车。守卫用雷达端点检查未来 0.8 秒内约 24×23 cm 的车体扫掠区域。它依赖雷达覆盖与实际制动能力，不能替代实物急停。恢复时保留静态墙体，重建相应全局或局部观测并等待 1 秒；仍被有效扫描观测到的障碍会重新标记，持续不可达时最终停止任务。

不要在导航运行时另开遥控节点直接发布 `/cmd_vel`；正常导航时此话题应只有 `velocity_guard` 一个发布者。

局部和全局 `obstacle_layer.scan` 的高度范围均显式设置为 **0.0–2.0 米**。车体实测约 18×17 厘米；配置矩形为 22×21 厘米，外加每侧 1 厘米 padding，发布轮廓约 24×23 厘米。当前仍需确认 `base_link` 相对实际外缘的偏置及所有外凸部件。URDF 中的底盘外形仍为旧标称尺寸，验收轮廓以实物测量为准，不能直接用 RViz 的 RobotModel 外观替代测量。

## 9. 故障排查

| 现象 | 检查与处理 |
| --- | --- |
| 导航一直等待 | 检查 A 中传感器；在 RViz 设置起点；查询 `/amcl`、`/bt_navigator` 生命周期是否为 `active` |
| 停在 `amcl/get_state service not available` | AMCL 可能已激活但状态响应丢失；新版任务节点每次查询等待最多 5 秒后重试，准备阶段无总超时。若持续重试，检查终端 B 是否运行及其 DDS 响应超时日志；重新设置位姿无法解决服务响应丢失 |
| `READY` 后没有运动 | 按回车或调用开始服务；这是准备状态，不计时 |
| 任务启动后位置跳到原点 | 确认已部署新版 `competition_manager`，默认保留 RViz 定位 |
| `Failed to make progress` 或转向缓慢 | 对比 `/cmd_vel_nav_raw`、`/cmd_vel`、`/odom`；检查定位和实际转向，避免只提高最高速度 |
| Nav2 成功但停留检查失败 | 日志中的 `position_error` 显示当前位置误差或 TF 不可用；`stationary` 显示静止判定。核对实际位置、定位跳变和里程计时效；不要直接放宽到达容差 |
| RViz 没地图 | 检查 `/map`、两端域编号 `6`、网络发现；Map 显示的 Durability 设为 Transient Local |
| 找不到包或配置 | 编译两个工作空间，并在当前终端加载 `install/setup.bash` |
| 恢复失败 | 检查路线、坐标文件是否变动，以及记录中的原轮时间预算是否已用完 |
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
| 只有单点超时 | 已实现整轮预算，测试默认 600 秒、比赛 180 秒，覆盖导航、恢复、重试和停留；超时取消并发送零速度 |
| 不强制四个目标 | 默认恰好四个；练习模式可显式放宽，重复字母按独立访问处理 |
| 字母坐标写死 | 已移至可替换 YAML，启动校验；地图变化后仍须重新测量 |
| 起点只能手动/数值设置 | 已增加起始格 + 罗盘朝向；需要先标定地图北向，默认仍用 RViz |
| 所有目标 yaw 为 0 | 默认按入站方向选择目标朝向，也支持固定朝向 |
| 到达只看 Nav2 结果 | 增加任务层位置检查、实测速度检查和连续停留；Nav2 配置明确位置容差 |
| 失败后没有继续方式 | 有限重试、显式跳点和检查点恢复；已用时间不因恢复清零 |
| 没有独立开始触发 | READY 后回车或服务开始；准备时间不计入新一轮 |
| SSH 断开会中断任务 | `start2.sh` / `start3.sh` 在当前终端运行，需保持 SSH 连接；`start1.sh` 仍使用 tmux |
| 部署依赖机器配置 | 增加只读部署检查；未知设备别名和系统服务仍需实验室提供正确配置 |

以下项目**仍须随后实车验收**，不能仅凭代码或软件测试认定通过：

- A–X 测量坐标是否与当前地图、实物中心标签对应；地图北向是否已标定。
- 10 厘米软件容差是否足以让实际车体覆盖中心标签。当前检查使用 `base_link` 参考点，不是摄像头或标签覆盖检测；须结合实物轮廓、定位误差及标签尺寸调整。
- 每点是否实际连续静止至少 3 秒，以及整轮是否在 180 秒内完成；当前速度阈值需结合传感器噪声验证。
- 转向加速度调整后的起转、停车与狭窄处通行表现；车体 footprint、传感器外参和电机响应是否准确。
- 对新增或动态障碍物的避让、重新规划及恢复效果；现有激光障碍层和碰撞预测需在场地验证。
- 超时或中断时的取消与停车延迟。软件发送取消/零速度不等于硬件实时急停，通信或驱动故障仍需实物停止手段。

本轮代码验收包括离线任务规则测试及隔离 ROS 域内的模拟动作测试；最终实车结果在完成上述测试后记录。程序没有摄像头字母识别或自动网格标定功能，这些功能不能通过修改现有坐标导航逻辑替代。

## 11. 本地独立窗口模拟

模拟运行在本机 **ROS_DOMAIN_ID=86**，使用 LOCALHOST 发现，与机器人使用的域 6 隔离。它使用 `simulator/maps/rb3302_map.yaml` 和配套图像重建迷宫，通过窗口显示墙体、A–X 格、激光点、车体与车头方向；不需要 RViz。

要求电脑安装 ROS 2 Jazzy、Nav2、robot_localization、colcon，以及系统 Python 的 `rclpy`、`yaml`、`PIL` 和 `tkinter`。每次启动在 `simulator/` 下增量构建导航、速度守卫和任务包，不使用机器人的编译产物。

在本地电脑的两个终端分别执行：

```bash
cd /media/lfzyzl/WinShare/Project/rb3302/rb3302_final_proj_code
./start_sim.sh
```

窗口打开后，在第二个本地终端运行：

```bash
cd /media/lfzyzl/WinShare/Project/rb3302/rb3302_final_proj_code
./sim_mission.sh
```

输入四个 A–X 字母；等待 `READY` 后再按回车开始。关闭模拟窗口或在第一个终端按 Ctrl+C 会关闭本地导航。若模拟器还未启动，先运行 `start_sim.sh`；已有实例必须先关闭。可用 `./start_sim.sh --headless` 在无窗口环境检查话题，或用 `./start_sim.sh --config /绝对路径/配置.yaml` 选择另一份配置。

在 `simulator/config.yaml` 的 `initial_pose` 修改 `x`、`y`（map 坐标，米）和 `yaw`（弧度，map 正 X 方向为 0，逆时针为正）。默认 F 点、题图向左；更改后重启模拟器生效。若初始车体与墙或未知区域重叠，程序会拒绝启动。地图坐标与 `student_ws/src/competition_manager/config/landmarks.yaml` 必须对应；地图变化需同步替换 simulator/maps 下的 YAML、PGM 并重新核对字母坐标。

模拟器订阅 `/cmd_vel`，发布 `/scan`、`/odom/raw`、`/imu_data_ros` 和静态 `base_link → laser` TF。Nav2 中的 EKF、AMCL、地图服务器及导航控制器与任务管理器产生其余定位和导航话题。初始位置同步用于虚拟车与 AMCL。车体触墙时模拟器阻止几何穿透，但这是理想化的二维模型：不模拟轮胎打滑、动力学、测距噪声、车体遮挡或通信延迟，不能用模拟成功替代实车避障验证。

`/sim/ground_truth` 额外提供模拟车在 map 坐标中的真实位置，方便与 `/amcl_pose` 对照；它不是实体小车话题。修正模拟定位噪声及迷宫前瞻距离后，无界面回归中 `EKNA` 与 `CJKL` 四点均第一次尝试完成，分别耗时约 97 秒、113 秒。模拟结果会随定位和控制器状态变化，不能把某次结果当作实车结论。

模拟定位参数单独位于 `simulator/config.yaml` 的 `localization`：默认使用理想里程计对应的较小 AMCL 运动噪声（alpha=0.01），初始位置标准差 2 cm、角度标准差 0.03 rad；这些值只写入 `simulator/log/nav2_sim_params.yaml`，不会修改实车 AMCL 参数。共享 RPP 配置使用 0.25 m 前瞻与 0.25 m 终点减速范围；位置容差统一 10 cm，不要求终点朝向，每点连续静止 3 秒。模拟只覆盖 AMCL 的理想里程噪声与初始化协方差，停车链路与实车相同。

模拟器每 0.5 秒把真值、地图定位、位置误差、指令速度、实际速度与几何接触状态写入 `simulator/log/ros/sim_trace_<PID>.jsonl`。任务到达复核失败时，日志会输出位置误差和是否静止。图形或扫描计算造成延迟时，运动模型按完整时间间隔分小步积分，并按实际完成运动发布里程计，避免丢失积分时间。关闭模拟窗口会终止专用进程组里的导航节点，释放实例锁。

## 12. 更新后的测试顺序

### 实车静态检查：先不运行 start3.sh

按第 1 节校时，启动 A、B 和电脑 RViz，设置实际位姿。小车保持静止，在另一个**机器人终端**执行：

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=6 ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_LOCALHOST_ONLY ROS_STATIC_PEERS
source ~/rb3302_xue/rb3302_final_proj_code/robot_ws/install/setup.bash
source ~/rb3302_xue/rb3302_final_proj_code/student_ws/install/setup.bash
for node in /amcl /bt_navigator /controller_server /planner_server; do
  echo "$node"
  ros2 lifecycle get "$node"
done
ros2 param get /amcl alpha1
ros2 param get /controller_server FollowPath.lookahead_dist
ros2 param get /controller_server goal_checker.stateful
ros2 param get /controller_server goal_checker.xy_goal_tolerance
ros2 param get /velocity_smoother feedback
ros2 node info /velocity_guard
ros2 topic info /cmd_vel --verbose
ros2 param get /controller_server FollowPath.use_collision_detection
ros2 param get /local_costmap/local_costmap obstacle_layer.scan.max_obstacle_height
ros2 param get /global_costmap/global_costmap obstacle_layer.scan.max_obstacle_height
ros2 param get /local_costmap/local_costmap footprint
ros2 param get /local_costmap/local_costmap footprint_padding
```

预期四个生命周期状态都是 `active [3]`；AMCL alpha1 为 **0.8**，前瞻 **0.25**，stateful **false**，碰撞检测 **true**，两个扫描源高度上限均 **2.0**；轮廓角点为 `(±0.11, ±0.105)`、padding 为 **0.01**。实车不应出现模拟专用 alpha=0.01 或 `/sim/ground_truth`。

在 RViz 添加一个 Map 显示，Topic 选择 `/local_costmap/costmap`，同时观察 `/scan` 与 `/local_costmap/published_footprint`。应能看到墙体对应的障碍格及其膨胀区域，并确认轮廓覆盖实际车身。只有雷达与静态地图重合，不能证明局部代价地图正常；如果局部地图一直全空、TF 不可用或定位明显跳动，先处理这些问题。

### 实车单目标，再四目标

第一次移动前，建议在额外的机器人终端记录数据；此命令本身不发送运动指令，测试结束按 Ctrl+C 停止录制：

```bash
source /opt/ros/jazzy/setup.bash
export ROS_DOMAIN_ID=6 ROS_AUTOMATIC_DISCOVERY_RANGE=SUBNET
unset ROS_LOCALHOST_ONLY ROS_STATIC_PEERS
mkdir -p "$HOME/.ros/rb3302/bags"
ros2 bag record -o "$HOME/.ros/rb3302/bags/test-$(date +%Y%m%d-%H%M%S)" \
  /scan /tf /tf_static /odom /odom/raw /amcl_pose /cmd_vel_nav_raw /cmd_vel_smoothed /cmd_vel_stop /cmd_vel /plan \
  /local_costmap/costmap /local_costmap/published_footprint
```

在前面的参数检查终端临时把期望直行速度设为 0.10 m/s，并核对设置成功：

```bash
ros2 param set /controller_server FollowPath.desired_linear_vel 0.10
ros2 param get /controller_server FollowPath.desired_linear_vel
```

在场地中放到 F、朝题图左方，在 RViz 对应设置实际位姿。运行 `./start3.sh --practice`，输入单个 `E`；READY 后再按回车。确认沿实际通道移动、到点后连续静止至少 3 秒，且没有碰墙或明显定位跳变。`--practice` 只改变目标数量，不会自动降低速度，上面的参数设置才控制本次期望直行速度；软件参数不等于实物急停。

单目标验证通过后，先停止任务，回到 F 并重新设置实际位姿，确认环境可控及可随时人工停止，再恢复常规期望速度并运行完整路线：

```bash
ros2 param set /controller_server FollowPath.desired_linear_vel 0.30
cd ~/rb3302_xue/rb3302_final_proj_code
./start3.sh
```

输入 `EKNA`，READY 后按回车。每个目标都要到位并连续静止 3 秒；四点完整完成才记录通过。再从 F 重新定位后测试 `CJKL`。两条路线的模拟回归耗时约 97 秒、113 秒，只作为软件回归记录，不是实车成绩。出现碰墙、重复恢复或停留复核失败时停止任务，保存 bag、`~/.ros/log` 和 `~/.ros/rb3302/last_mission.json`，不要直接放宽容差或延长计时来掩盖失败。

### 本地模拟回归

本地关闭旧模拟窗口后重新执行第 11 节的两个脚本。每条路线都从配置中的 F 初始位姿重新启动，分别输入 `EKNA`、`CJKL`；检查四点均完成、每点停留达标以及结果文件 `~/.ros/rb3302/sim_last_mission.json`。模拟使用域 86，轨迹在本地 `simulator/log/ros/`；实车使用域 6 和单独的结果文件，两者不要混为一轮测试。


### 本次更新后的部署与复测

更新源码后必须重新构建新增的速度守卫入口，并关闭旧的导航进程后再重启。仅重新进入原 tmux 会话不会加载新链路。机器人终端执行：

```bash
cd ~/rb3302_xue/rb3302_final_proj_code/student_ws
source /opt/ros/jazzy/setup.bash
colcon build --symlink-install --packages-select competition_manager planning_rpp
```

先在导航终端 B 按 Ctrl+C 结束旧导航，再从项目目录执行 `./start2.sh`。保留正常运行的硬件终端 A。用 RViz 重新设置实际位姿，核对上文生命周期与参数检查：XY 为 0.10、平滑器为 OPEN_LOOP，`/cmd_vel` 发布者仅为 velocity_guard。守卫打印 `command_timeout` 在尚未发目标时属于正常停车状态；发目标后应变为 `clear`。出现 `scan_unavailable` 先检查扫描与 TF，不能通过关闭守卫继续运行。

本地执行 `./start_sim.sh`，另开终端执行 `./sim_mission.sh`。分别从 F 初始位置重新启动后测试 CJKL、EKNA，确认四点完成、每点静止至少 3 秒、轨迹没有几何接触。模拟域 86 与实车域 6 保持隔离。实车先按上文单目标低速流程复测，再运行四目标；同步文件不会自动发送目标或启动运动。

到点边界修正：Nav2 成功后若新定位持续在 10 cm 圈外且车体静止，0.5 秒后进入导航重试，不再空等 15 秒。若重试时已在原目标 20 cm 内，导航精修目标沿当前位置到原目标的方向延伸最多 3 cm；记录和静止验收仍使用原始字母坐标及 10 cm 容差，不能把圈外位置计为完成。


本次本地回归（2026-11-03）：固定同一份配置、分别从 F 初始位姿运行，CJKL 完成约 71.2 秒（C、L 边界精修重试），EKNA 完成约 72.3 秒（E 边界精修重试）。每点均按原始坐标、10 cm 容差验证连续静止至少 3 秒。两轮采样轨迹没有几何接触，最大最终指令 0.20 m/s、0.80 rad/s。52 项任务、守卫、ROS 动作集成与模拟运动回归通过；另在域 87 验证异常反馈限速、零速、停车请求、障碍、扫描丢失和指令丢失。模拟耗时只作软件验证，不能作为实机性能保证。

升级后的任务在 READY 前还会等待 `/velocity_guard/ready` 确认雷达和 TF 新鲜；等待没有总准备超时。若一直提示重启 start2，表示仍在运行旧导航链路，请先按上述步骤重启终端 B。
