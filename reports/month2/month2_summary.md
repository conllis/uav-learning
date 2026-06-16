# 第 2 个月总结：从姿态控制到 PX4 外部控制入门

## 一、本月学习目标

第 2 个月的主要目标是：在第 1 个月已经完成 PX4 SITL、Gazebo、QGroundControl、基础 PID 和四旋翼基础理解的基础上，继续向“用程序读取和控制 PX4 SITL”推进。

本月学习主线是：

```text
姿态 PID
    ↓
角速度控制
    ↓
级联控制
    ↓
MAVLink / MAVSDK
    ↓
Telemetry 读取
    ↓
Action 控制
    ↓
Offboard 控制概念
    ↓
ROS2 / 传感器 / STM32 预备
```

本月最重要的目标是：

```text
从“理解无人机怎么飞”
升级到
“能用代码读取 PX4 状态，并尝试控制 PX4 SITL 飞行”
```

---

## 二、本月完成内容

## 1. 姿态 PID 与级联控制入门

本月前半部分学习了姿态控制。

之前已经做过高度 PID：

```text
目标高度
    ↓
当前高度
    ↓
高度误差
    ↓
PID
    ↓
推力
    ↓
加速度 / 速度 / 高度
```

本月进一步学习了 roll 和 pitch 姿态 PID：

```text
目标姿态角
    ↓
当前姿态角
    ↓
姿态角误差
    ↓
PID
    ↓
力矩
    ↓
角加速度
    ↓
角速度
    ↓
姿态角
```

完成了：

```text
roll 单轴姿态 PID 仿真
pitch 单轴姿态 PID 仿真
姿态角和角速度关系理解
级联控制理解
roll / pitch 仿真 README
第 1 周姿态控制总结
```

对应项目目录：

```text
code/02_attitude_pid_sim/
```

本阶段最重要的理解是：

```text
高度控制输出推力；
姿态控制输出力矩；
姿态控制通常不是直接到电机，而是经过姿态环、角速度环、控制分配，最后才到电机输出。
```

PX4 中可以理解为：

```text
vehicle_attitude_setpoint
    ↓
Attitude Controller
    ↓
vehicle_rates_setpoint
    ↓
Rate Controller
    ↓
vehicle_torque_setpoint
    ↓
Control Allocation
    ↓
actuator_motors
```

---

## 2. MAVLink / MAVSDK 基础理解

本月学习了 MAVLink 和 MAVSDK 的关系。

MAVLink 是无人机通信协议。

MAVSDK 是基于 MAVLink 的开发库。

可以这样理解：

```text
MAVLink = 无人机通信语言
MAVSDK = 帮程序员使用这门语言的工具包
```

QGroundControl、MAVSDK、ROS2 以后都可能通过 MAVLink 或相关桥接方式和 PX4 交换数据。

本阶段理解了：

```text
Telemetry：读取无人机状态
Action：发送高级动作命令
Offboard：持续发送 setpoint 控制目标
```

---

## 3. PX4 SITL MAVLink 端口确认

本月启动 PX4 SITL，并确认了 MAVLink 端口。

启动命令：

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

在 PX4 终端中查看：

```bash
mavlink status
```

确认了 MAVSDK 常用连接地址：

```text
udp://:14540
```

后面也发现新版 MAVSDK 会提示：

```text
udp:// 已弃用，建议使用 udpin:// 或 udpout://
```

因此后续可以优先使用：

```python
await drone.connect(system_address="udpin://0.0.0.0:14540")
```

---

## 4. MAVSDK Python 安装与连接测试

本月创建了 MAVSDK Python 项目目录：

```text
code/03_mavsdk_telemetry/
```

并完成了 Python 虚拟环境和 MAVSDK 安装：

```bash
cd ~/uav-learning
mkdir -p code/03_mavsdk_telemetry
cd code/03_mavsdk_telemetry
python3 -m venv venv
source venv/bin/activate
pip install mavsdk
```

完成连接测试程序：

```text
connect_test.py
```

程序核心流程：

```text
创建 System 对象
    ↓
连接 PX4 SITL
    ↓
等待 connection_state
    ↓
确认 Drone connected
```

本阶段最重要的理解：

```text
System 表示一架无人机；
connect() 负责连接 PX4；
async / await 用于处理无人机这种持续通信任务；
async for 用于持续读取 telemetry 数据流。
```

---

## 5. 读取 PX4 Telemetry

本月完成了基础 telemetry 读取。

读取内容包括：

```text
armed
flight_mode
position
relative_altitude_m
roll
pitch
yaw
```

程序：

```text
read_basic_telemetry.py
```

理解到：

```text
Telemetry 是 PX4 发给外部程序的状态信息。
```

也就是：

```text
PX4 → MAVLink → MAVSDK → Python
```

本阶段最重要的收获是：已经可以用 Python 程序看到 PX4 SITL 的实时状态。

---

## 6. 保存 Telemetry 到 CSV 并画图

本月完成了 telemetry 数据保存：

```text
log_telemetry_csv.py
```

输出文件：

```text
data/px4_telemetry.csv
```

保存字段包括：

```text
time_s
armed
flight_mode
latitude_deg
longitude_deg
absolute_altitude_m
relative_altitude_m
roll_deg
pitch_deg
yaw_deg
```

后续又完成了绘图脚本：

```text
scripts/plot_telemetry.py
```

生成：

```text
relative_altitude.png
attitude_euler.png
flight_mode.png
```

本阶段最重要的理解：

```text
飞控实验不能只看现象，还要记录数据；
CSV 是保存实验过程的基础；
曲线可以帮助分析高度、姿态和模式变化。
```

---

## 7. MAVSDK Action 控制 PX4 SITL

本月从“读取状态”进入“发送控制命令”。

学习了 MAVSDK Action：

```python
await drone.action.arm()
await drone.action.takeoff()
await drone.action.land()
await drone.action.return_to_launch()
await drone.action.set_takeoff_altitude(3.0)
```

完成程序：

```text
action_status_check.py
action_arm_takeoff.py
action_takeoff_hover_land.py
action_takeoff_hover_land_log.py
```

实现了：

```text
连接 PX4
等待 health ready
设置起飞高度
arm 解锁
takeoff 起飞
hover 悬停
land 降落
全过程记录 telemetry
```

本阶段最重要的理解是：

```text
Action 发命令；
Telemetry 看结果。
```

例如：

```python
await drone.action.takeoff()
```

只是发送起飞命令，不代表无人机已经到达目标高度。

必须通过：

```text
relative_altitude_m
flight_mode
armed
```

判断动作是否真的完成。

---

## 8. 边控制边记录 Telemetry

本月完成了一个综合任务：

```text
Action 控制无人机起飞 / 悬停 / 降落
同时持续记录 telemetry 到 CSV
```

程序：

```text
action_takeoff_hover_land_log.py
```

输出文件：

```text
data/takeoff_hover_land_telemetry.csv
```

其中增加了重要字段：

```text
mission_phase
```

用于标记任务阶段：

```text
init
arming
takeoff
hover
landing
finished
```

这个字段的意义是：

```text
后续画图时，可以知道哪一段是起飞，哪一段是悬停，哪一段是降落。
```

这一步让实验从“能飞”变成“能分析”。

---

## 9. Action 控制 README 整理

本月整理了项目文档：

```text
README_action_control.md
```

说明了：

```text
项目目标
项目背景
核心程序作用
运行方法
CSV 字段含义
mission_phase 含义
Action 和 Telemetry 的关系
当前不足
后续改进方向
```

这一步的意义是：

```text
把零散代码整理成可以复现、可以展示、可以继续扩展的项目。
```

---

## 10. Offboard 控制概念与最小实验准备

本月开始进入 Offboard 控制。

理解到：

```text
Action 是高级动作命令；
Offboard 是持续发送 setpoint。
```

Action 适合：

```text
起飞
降落
返航
```

Offboard 适合：

```text
悬停
移动到指定点
轨迹跟踪
视觉引导
避障
外部路径规划
```

Offboard 的基本流程是：

```text
连接 PX4
    ↓
等待 health ready
    ↓
Action 起飞
    ↓
先发送初始 setpoint
    ↓
start Offboard
    ↓
持续发送 / 更新 setpoint
    ↓
stop Offboard
    ↓
Action 降落
```

本月尝试了：

```text
offboard_hover.py
offboard_move_point.py
```

目标是：

```text
Offboard 悬停
Offboard 移动到一个点
```

实验中发现起飞阶段高度上升较慢，但已经确认：

```text
PX4 能连接
health ready 正常
arm 成功
takeoff 命令成功
PX4 进入 TAKEOFF 模式
Gazebo 有播放
无人机有离地
```

该问题后续可以作为：

```text
仿真性能
PX4 参数
起飞速度
Offboard 调试
```

继续排查。

---

## 11. ROS2 入门

本月开始准备 ROS2。

理解到：

```text
ROS2 是机器人系统的通信和组织框架。
```

ROS2 的核心不是直接控制电机，而是让多个机器人程序协作。

核心概念包括：

```text
Node
Topic
Message
Publisher
Subscriber
Service
Action
Workspace
Package
```

无人机系统中可以有：

```text
camera_node
detect_node
localization_node
planner_node
control_node
logger_node
```

这些节点通过 topic、service、action 进行通信。

本阶段最重要的理解：

```text
MAVSDK 适合直接连接 PX4 做控制实验；
ROS2 适合组织复杂机器人系统，让感知、规划、控制、记录等模块协同工作。
```

---

## 12. 传感器和滤波入门

本月学习了无人机传感器和滤波基础。

常见传感器包括：

```text
IMU
气压计
GPS
磁力计
光流
激光 / 超声波
相机
```

理解到原始传感器数据存在：

```text
噪声
偏置
漂移
延迟
丢失
异常值
```

所以飞控不能直接相信原始数据，而要进行：

```text
滤波
融合
状态估计
```

本阶段学习了：

```text
滑动平均滤波
低通滤波
互补滤波
EKF 基本概念
```

PX4 中可以理解为：

```text
传感器
    ↓
滤波 / 融合
    ↓
EKF2
    ↓
vehicle_attitude
vehicle_local_position
vehicle_global_position
    ↓
控制器
```

最重要的结论：

```text
传感器负责测量世界；
滤波负责减小噪声；
EKF 负责融合多源数据；
控制器根据估计状态控制无人机。
```

---

## 13. STM32 / FreeRTOS 预备

本月最后学习了 STM32 和 FreeRTOS 的基础概念。

STM32 是常见微控制器，常用于飞控板、机器人控制器、电机控制板和传感器采集板。

FreeRTOS 是实时操作系统，用于把嵌入式程序拆成多个实时任务。

理解了：

```text
Task
Scheduler
Interrupt
实时性
任务优先级
嵌入式飞控
```

飞控中可能有：

```text
IMU 读取任务
姿态估计任务
控制器任务
电机输出任务
通信任务
日志任务
安全检查任务
```

本阶段最重要的理解：

```text
STM32 负责靠近硬件；
FreeRTOS 负责任务调度；
PX4 负责飞控逻辑；
真实飞控系统非常重视实时性。
```

---

# 三、本月项目成果

## 1. 姿态 PID 项目

```text
code/02_attitude_pid_sim/
```

包含：

```text
roll_pid_sim.cpp
pitch_pid_sim.cpp
PIDController.hpp
PIDController.cpp
plot_roll_pid.py
plot_pitch_pid.py
README.md
```

完成能力：

```text
理解高度 PID 和姿态 PID 的区别
理解姿态角、角速度、力矩关系
理解 roll / pitch 单轴控制
理解级联控制基本结构
```

---

## 2. MAVSDK Telemetry / Action / Offboard 项目

```text
code/03_mavsdk_telemetry/
```

包含：

```text
connect_test.py
read_basic_telemetry.py
log_telemetry_csv.py
plot_telemetry.py
action_status_check.py
action_arm_takeoff.py
action_takeoff_hover_land.py
action_takeoff_hover_land_log.py
offboard_hover.py
offboard_move_point.py
README_action_control.md
```

完成能力：

```text
连接 PX4 SITL
读取 telemetry
保存 CSV
绘制 telemetry 曲线
发送 Action 命令
完成起飞 / 悬停 / 降落流程
边控制边记录数据
理解 Offboard setpoint
尝试 Offboard 悬停和移动
```

---

## 3. 传感器滤波小实验

```text
code/04_sensor_filter_basic/
```

包含：

```text
low_pass_filter_demo.py
```

完成能力：

```text
理解低通滤波
理解 alpha 参数影响
理解原始数据和滤波数据的区别
```

---

# 四、本月笔记和报告

本月主要笔记包括：

```text
notes/control/day32_roll_pid.md
notes/control/day33_pitch_pid.md
notes/control/day34_rate_control_basic.md
notes/control/day35_cascade_control.md

notes/mavlink/day38_mavlink_mavsdk_basic.md
notes/mavlink/day39_px4_mavlink_port.md
notes/mavlink/day40_mavsdk_python_install_test.md
notes/mavlink/day41_read_basic_telemetry.md
notes/mavlink/day42_log_telemetry_csv.md
notes/mavlink/day43_plot_telemetry.md
notes/mavlink/day45_mavsdk_action_basic.md
notes/mavlink/day46_mavsdk_arm_takeoff.md
notes/mavlink/day47_takeoff_hover_land.md
notes/mavlink/day48_control_and_log_telemetry.md

notes/offboard/day50_offboard_concept.md
notes/offboard/day52_offboard_minimal_experiment.md

notes/ros2/day55_ros2_basic.md
notes/sensors/day56_sensor_filter_basic.md
notes/embedded/day57_stm32_freertos_basic.md
```

本月报告包括：

```text
reports/month2/week1_attitude_control_summary.md
reports/month2/week2_mavsdk_telemetry_summary.md
reports/month2/week3_mavsdk_action_summary.md
reports/month2/month2_summary.md
```

---

# 五、本月最重要的理解

## 1. 从控制理论到 PX4 数据流

本月理解到，无人机控制不是一个简单 PID，而是多层级联系统。

可以概括为：

```text
位置目标
    ↓
速度目标
    ↓
加速度 / 推力目标
    ↓
姿态目标
    ↓
角速度目标
    ↓
力矩 / 推力
    ↓
电机输出
```

---

## 2. 从“看状态”到“发命令”

本月完成了一个重要转变：

```text
Telemetry：读取状态
Action：发送命令
Offboard：持续发送目标
```

这意味着已经从“观察 PX4”进入“控制 PX4”。

---

## 3. Action 和 Offboard 的区别

Action：

```text
高级动作命令
适合起飞、降落、返航
通常发送一次
```

Offboard：

```text
持续发送 setpoint
适合位置控制、速度控制、轨迹控制
必须持续发送目标
```

---

## 4. 数据记录很重要

本月理解到，飞控实验不能只看 Gazebo 里的现象。

必须记录：

```text
高度
姿态
飞行模式
解锁状态
任务阶段
时间
```

因为只有保存数据，才能分析：

```text
是否达到目标高度
是否稳定悬停
是否有超调
是否有震荡
模式是否正常切换
```

---

## 5. 真实飞控不仅有算法，还有硬件和实时系统

通过传感器、滤波、STM32、FreeRTOS 的学习，理解到真实飞控系统包括：

```text
传感器测量
滤波
状态估计
控制器
实时任务调度
嵌入式硬件
电机输出
```

飞控不是单纯的软件脚本，而是一个软硬件结合的实时系统。

---

# 六、本月存在的问题

目前还存在以下问题：

```text
1. Offboard 最小实验还没有完全稳定跑通；
2. 起飞阶段高度上升偏慢的问题还没有彻底定位；
3. 还没有对 takeoff_hover_land_telemetry.csv 进行更完整的阶段曲线分析；
4. ROS2 目前只完成概念和安装准备，还没有创建自己的 ROS2 package；
5. 传感器滤波只做了基础理解，还没有和 PX4 telemetry 数据结合；
6. STM32 / FreeRTOS 只完成概念预备，还没有进入实际开发环境；
7. 对 PX4 内部源码和模块还只是初步理解；
8. 对真实飞控硬件还没有实际操作经验。
```

---

# 七、下个月学习计划

第 3 个月建议围绕以下方向展开：

```text
1. ROS2 基础实操
2. 创建 ROS2 workspace 和 package
3. 编写 publisher / subscriber
4. 用 ROS2 发布模拟无人机状态
5. 用 ROS2 订阅目标 setpoint
6. 继续完善 Offboard 控制实验
7. 记录 Offboard telemetry 并画图
8. 学习 PX4 ROS2 Bridge 或 MAVROS 基础
9. 继续学习传感器滤波小实验
10. 开始 STM32 / FreeRTOS 环境准备
```

第 3 个月目标：

```text
从“单独用 Python 控制 PX4”
升级到
“理解 ROS2 多节点机器人系统，并逐步把无人机控制接入 ROS2 思路”
```

---

# 八、本月总结

第 2 个月完成了从基础 PID 到 PX4 外部控制入门的过渡。

本月已经具备的能力：

```text
理解姿态 PID
理解角速度控制
理解级联控制
理解 MAVLink / MAVSDK
能连接 PX4 SITL
能读取 telemetry
能保存 CSV
能绘制 telemetry 曲线
能用 Action 控制 PX4 起飞、悬停、降落
能边控制边记录数据
理解 Offboard setpoint 控制思想
理解 ROS2 基础概念
理解传感器和滤波基础
理解 STM32 / FreeRTOS 为什么和飞控有关
```

本月最重要的成果是：

```text
已经从“仿真和控制理论学习”
进入
“用外部程序读取、控制、记录 PX4 SITL”
```

一句话总结：

```text
第 2 个月的核心成果是：完成了从姿态控制基础到 MAVSDK 控制 PX4 SITL 的阶段跨越，并为后续 ROS2、Offboard、传感器融合和嵌入式飞控学习打下基础。
```
