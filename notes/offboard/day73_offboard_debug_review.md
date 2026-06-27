# Day 73 Offboard 问题记录与稳定流程整理

## 今日目标

今天不急着写新的 Offboard 轨迹代码，而是先整理之前 Offboard 调试中可能遇到的问题，并确定后续统一实验流程。

后续 Offboard 实验统一采用：

```text
Action 起飞
    ↓
Offboard 接管
    ↓
发送位置 setpoint
    ↓
记录 telemetry
    ↓
Action 降落
1. 为什么今天不直接写 Offboard 轨迹？

Offboard 控制对流程要求比较严格。

如果没有先整理好连接、起飞、setpoint、降落和日志记录流程，后面容易出现这些问题：

MAVSDK 连接不上 PX4
PX4 没有成功进入 TAKEOFF
Gazebo 没有播放
无人机没有离地
高度上升很慢
Offboard 进入失败
setpoint 没有持续发送
进入 Offboard 后马上退出
没有记录 telemetry，导致无法分析问题

所以今天的任务是先把流程固定下来，让后面 Day 74、Day 75、Day 76 的实验更稳定。

2. PX4 SITL 检查项

启动命令：

cd ~/PX4-Autopilot
make px4_sitl gz_x500

需要检查：

Gazebo 是否打开：
Gazebo 是否处于播放状态：
PX4 终端是否出现 pxh>：
无人机模型是否正常显示：
是否有明显报错：

记录：

PX4 SITL 启动结果：
Gazebo 是否正常：
PX4 是否进入 pxh>：
问题记录：
3. MAVSDK 连接检查项

后续 Offboard 代码优先使用：

CONNECTION_URL = "udpin://0.0.0.0:14540"

如果连接不上，再尝试：

CONNECTION_URL = "udp://:14540"

需要检查：

是否出现 PX4 discovered and connected
是否能读取 telemetry
是否能读取 flight mode
是否能读取 altitude

记录：

当前使用连接地址：
是否连接成功：
是否能读取 telemetry：
问题记录：
4. Action 起飞检查项

后续不建议直接用 Offboard 从地面硬起飞，而是先用 MAVSDK Action 起飞到安全高度。

测试命令：

ros2 topic pub --once /uav/action_command std_msgs/msg/String "{data: 'takeoff'}"

需要检查：

是否 arm 成功：
是否进入 TAKEOFF：
是否离地：
高度是否上升：
目标高度是多少：
是否能接近目标高度：
起飞是否过慢：

记录：

是否成功 arm：
是否进入 TAKEOFF：
是否离地：
目标高度：
实际高度变化：
问题记录：
5. Action 降落检查项

降落命令：

ros2 topic pub --once /uav/action_command std_msgs/msg/String "{data: 'land'}"

需要检查：

是否进入 LAND：
是否开始下降：
是否落地：
是否能安全结束：

记录：

是否进入 LAND：
是否开始下降：
是否落地：
问题记录：
6. Offboard 接管前检查项

Offboard 模式不能随便进入。

进入 Offboard 前必须注意：

先持续发送一段时间 setpoint
再调用 Offboard start
进入 Offboard 后继续持续发送 setpoint
setpoint 不能中断
如果异常，必须自动 land

后续检查：

是否先发送 setpoint：
是否成功进入 Offboard：
进入 Offboard 后是否持续发送 setpoint：
是否能保持高度：
异常时是否能 land：
7. 后续稳定实验流程

后续 Offboard 实验统一采用以下流程：

1. 启动 PX4 SITL
2. 等待 Gazebo 正常播放
3. MAVSDK 连接 PX4
4. 检查 health
5. Action 设置起飞高度
6. Action arm
7. Action takeoff
8. 等待无人机接近目标高度
9. 开始持续发送 Offboard setpoint
10. 进入 Offboard 模式
11. 执行悬停 / 移动 / 方形轨迹
12. 记录 telemetry CSV
13. Action land 降落
8. Day 74 稳定版 Offboard 悬停代码要求

Day 74 的 offboard_hover_stable.py 至少要满足：

使用稳定连接地址
有清楚的阶段打印
有超时机制
有 telemetry 记录
有异常保护
最后必须自动 land

推荐阶段：

CONNECTING
CONNECTED
WAITING_HEALTH
ARMING
TAKEOFF
WAITING_ALTITUDE
STARTING_OFFBOARD
HOVERING
LANDING
FINISHED
ERROR

CSV 建议字段：

time_sec, relative_altitude_m, roll_deg, pitch_deg, yaw_deg, mission_phase
9. Action 和 Offboard 的分工
Action 适合做什么？

Action 适合做高级动作：

arm
takeoff
land
return to launch
Offboard 适合做什么？

Offboard 适合做持续控制：

持续发送位置 setpoint
持续发送速度 setpoint
悬停
移动到点
方形轨迹
轨迹跟踪
后续原则
Action 负责起飞和降落
Offboard 负责中间的持续轨迹控制

这样流程更稳定，也更容易排查问题。

10. 今日结论

后续第 3 周 Offboard 实验统一采用：

Action 起飞 + Offboard 接管 + Action 降落

今天不追求新轨迹，而是先保证后续实验流程稳定、可记录、可复现。

11. 今日完成情况
是否完成 Offboard 问题整理：
是否明确稳定流程：
是否确认连接地址：
是否确认后续采用 Action 起飞：
是否确认后续采用 Offboard 接管：
是否确认后续采用 Action 降落：
遇到的问题：

---

# 2. 今天建议做一次最小验证

今天不需要进入 Offboard，只需要验证 **PX4 SITL + Action 起飞 / 降落** 是否稳定。

## 终端 1：启动 PX4 SITL

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500

等待 Gazebo 打开。

终端 2：启动 Action command node
cd ~/uav-learning/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 run uav_mavsdk_bridge px4_action_command_node

如果你是 Jazzy：

source /opt/ros/jazzy/setup.bash
source install/setup.bash

ros2 run uav_mavsdk_bridge px4_action_command_node
终端 3：发送状态检查
cd ~/uav-learning/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash

ros2 topic pub --once /uav/action_command std_msgs/msg/String "{data: 'status'}"

记录输出里的：

connected
in_air
flight_mode
relative altitude
roll / pitch / yaw
health
终端 3：发送起飞命令
ros2 topic pub --once /uav/action_command std_msgs/msg/String "{data: 'takeoff'}"

观察并记录：

是否 arm
是否进入 TAKEOFF
是否离地
高度是否上升
Gazebo 是否播放
终端 3：发送降落命令
ros2 topic pub --once /uav/action_command std_msgs/msg/String "{data: 'land'}"

观察并记录：

是否进入 LAND
是否下降
是否落地
3. 如果今天发现问题，先这样处理

如果 MAVSDK 一直连接不上，把代码里的连接地址改成：

CONNECTION_URL = "udpin://0.0.0.0:14540"

然后重新编译：

cd ~/uav-learning/ros2_ws
colcon build --packages-select uav_mavsdk_bridge
source install/setup.bash

如果 health 检查不通过，先不要强行起飞，等待 PX4 SITL 初始化完成。

如果 Gazebo 没有播放，确认 Gazebo 窗口左下角不是暂停状态。

如果起飞很慢，今天先记录现象，不要卡住。后面 Day 74 的稳定版 Offboard 悬停脚本会加入阶段记录和超时逻辑。

4. 今日完成标准

今天完成后，你应该有：

notes/offboard/day73_offboard_debug_review.md

并且里面写清楚：

1. Offboard 常见问题
2. PX4 / Gazebo / MAVSDK 检查项
3. Action 起飞检查项
4. Action 降落检查项
5. Offboard 接管前检查项
6. 后续统一流程：Action 起飞 + Offboard 接管 + Action 降落
