# MAVSDK Action Control：PX4 SITL 自动起飞、悬停、降落与 Telemetry 记录

## 1. 项目目标

本项目用于学习如何使用 MAVSDK Python 控制 PX4 SITL 仿真无人机完成基础飞行动作。

本项目重点完成：

```text
连接 PX4 SITL
读取 telemetry
使用 Action 解锁
使用 Action 起飞
起飞后悬停
使用 Action 降落
边飞行边记录 telemetry 到 CSV
```

本项目的核心理解是：

```text
Telemetry 用来读取无人机状态；
Action 用来向 PX4 发送高级动作命令；
CSV 用来保存飞行全过程数据；
曲线用来分析飞行过程。
```

---

## 2. 项目背景

前期已经完成 MAVSDK Telemetry 学习，包括：

```text
连接 PX4 SITL
读取 position
读取 attitude_euler
读取 flight_mode
读取 armed
保存 telemetry 到 CSV
绘制 telemetry 曲线
```

在此基础上，本项目进一步学习 MAVSDK Action 控制。

Action 控制不是直接控制电机，而是向 PX4 发送高级飞行动作命令。

例如：

```text
arm：解锁
takeoff：自动起飞
land：自动降落
return_to_launch：返航
```

真正的高度控制、姿态控制、角速度控制和电机输出，仍然由 PX4 内部控制器完成。

---

## 3. 项目目录结构

```text
code/03_mavsdk_telemetry/
├── venv/
├── connect_test.py
├── read_basic_telemetry.py
├── log_telemetry_csv.py
├── action_status_check.py
├── action_arm_takeoff.py
├── action_takeoff_hover_land.py
├── action_takeoff_hover_land_log.py
├── data/
│   ├── px4_telemetry.csv
│   └── takeoff_hover_land_telemetry.csv
├── scripts/
│   └── plot_telemetry.py
├── plots/
│   ├── relative_altitude.png
│   ├── attitude_euler.png
│   └── flight_mode.png
└── README_action_control.md
```

---

## 4. 核心程序说明

### 4.1 connect_test.py

作用：

```text
测试 MAVSDK Python 是否能连接 PX4 SITL。
```

核心功能：

```text
创建 System 对象
连接 udp://:14540
等待 Drone connected
```

成功标志：

```text
Drone connected!
```

---

### 4.2 read_basic_telemetry.py

作用：

```text
读取 PX4 SITL 的基础 telemetry。
```

读取内容：

```text
position
attitude_euler
flight_mode
armed
```

对应含义：

```text
position：位置、高度
attitude_euler：roll、pitch、yaw
flight_mode：飞行模式
armed：是否解锁
```

---

### 4.3 log_telemetry_csv.py

作用：

```text
读取 telemetry 并保存到 CSV。
```

输出文件：

```text
data/px4_telemetry.csv
```

保存字段：

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

---

### 4.4 action_status_check.py

作用：

```text
检查 PX4 当前状态，但不执行起飞。
```

主要读取：

```text
armed
flight_mode
relative_altitude_m
```

该程序用于确认：

```text
PX4 已连接
Telemetry 正常
Action 控制前状态可读
```

---

### 4.5 action_arm_takeoff.py

作用：

```text
实现自动解锁和起飞。
```

流程：

```text
连接 PX4
等待 health ready
设置起飞高度
arm 解锁
takeoff 起飞
读取 relative_altitude_m
判断是否接近目标高度
```

核心理解：

```text
takeoff() 只是发送起飞命令；
是否真的起飞，要通过 relative_altitude_m 判断。
```

---

### 4.6 action_takeoff_hover_land.py

作用：

```text
实现完整自动飞行流程。
```

流程：

```text
arm
takeoff
hover
land
```

即：

```text
解锁 → 起飞 → 悬停 → 降落
```

该程序完成了 PX4 SITL 的基础 Action 控制闭环。

---

### 4.7 action_takeoff_hover_land_log.py

作用：

```text
边控制无人机，边记录 telemetry 到 CSV。
```

流程：

```text
启动 telemetry observer
启动 CSV logger
arm 解锁
takeoff 起飞
hover 悬停
land 降落
保存全过程数据
```

输出文件：

```text
data/takeoff_hover_land_telemetry.csv
```

该程序是本阶段最重要的综合程序。

---

## 5. MAVSDK 连接地址

Day 39 中，PX4 的 MAVLink 状态显示：

```text
instance #1:
mode: Onboard
UDP local port: 14580
remote port: 14540
```

因此本项目使用 MAVSDK Python 连接地址：

```text
udp://:14540
```

Python 代码中写法：

```python
await drone.connect(system_address="udp://:14540")
```

如果连接失败，可以尝试：

```python
await drone.connect(system_address="udpin://0.0.0.0:14540")
```

---

## 6. 运行环境

### 6.1 启动 PX4 SITL

第一个终端：

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

等待 Gazebo 打开，并确认 PX4 正常运行。

---

### 6.2 激活 Python 虚拟环境

第二个终端：

```bash
cd ~/uav-learning/code/03_mavsdk_telemetry
source venv/bin/activate
```

检查 MAVSDK：

```bash
python -c "import mavsdk; print('mavsdk ok')"
```

---

## 7. 运行 Action 控制程序

### 7.1 状态检查

```bash
python action_status_check.py
```

作用：

```text
只读取状态，不起飞。
```

---

### 7.2 自动解锁 + 起飞

```bash
python action_arm_takeoff.py
```

作用：

```text
自动 arm
自动 takeoff
等待高度接近目标高度
```

成功标志：

```text
Armed successfully.
Takeoff command sent.
Target takeoff altitude reached.
```

---

### 7.3 起飞 + 悬停 + 降落

```bash
python action_takeoff_hover_land.py
```

作用：

```text
自动完成 解锁 → 起飞 → 悬停 → 降落
```

成功标志：

```text
Armed successfully.
Takeoff command sent.
Land command sent.
Drone is near ground.
```

---

### 7.4 边控制边记录 telemetry

```bash
python action_takeoff_hover_land_log.py
```

作用：

```text
自动完成 解锁 → 起飞 → 悬停 → 降落
同时记录全过程 telemetry 到 CSV
```

输出文件：

```text
data/takeoff_hover_land_telemetry.csv
```

---

## 8. CSV 数据说明

`takeoff_hover_land_telemetry.csv` 保存字段：

```text
time_s
mission_phase
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

字段含义：

```text
time_s：程序运行时间
mission_phase：当前任务阶段
armed：是否解锁
flight_mode：飞行模式
latitude_deg：纬度
longitude_deg：经度
absolute_altitude_m：绝对高度
relative_altitude_m：相对起飞点高度
roll_deg：横滚角
pitch_deg：俯仰角
yaw_deg：偏航角
```

其中最重要的是：

```text
mission_phase
relative_altitude_m
roll_deg
pitch_deg
yaw_deg
flight_mode
armed
```

---

## 9. mission_phase 说明

`mission_phase` 用于标记当前任务阶段。

常见阶段：

```text
init
set_takeoff_altitude
arming
takeoff
hover
landing
finished
action_error
interrupted
```

它的作用是帮助后续分析飞行过程。

例如：

```text
takeoff 阶段：高度应该上升
hover 阶段：高度应该基本稳定
landing 阶段：高度应该下降
```

---

## 10. Action 和 Telemetry 的关系

本项目最核心的理解是：

```text
Action 发命令；
Telemetry 看结果。
```

例如：

```python
await drone.action.takeoff()
```

这行代码只是向 PX4 发送起飞命令。

它不代表无人机已经到达目标高度。

因此还需要读取：

```python
position.relative_altitude_m
```

判断高度是否真的上升。

同理：

```python
await drone.action.land()
```

只是发送降落命令。

是否真的降落完成，需要观察：

```text
relative_altitude_m 是否接近 0
flight_mode 是否变化
armed 状态是否变化
```

---

## 11. 本项目和 PX4 内部控制器的关系

MAVSDK Action 并不直接控制电机。

调用：

```python
await drone.action.takeoff()
```

实际流程可以理解为：

```text
Python 程序
    ↓
MAVSDK Action
    ↓
MAVLink 命令
    ↓
PX4 Commander
    ↓
PX4 Position Controller
    ↓
PX4 Attitude Controller
    ↓
PX4 Rate Controller
    ↓
Control Allocation
    ↓
actuator_motors
    ↓
Gazebo 无人机起飞
```

也就是说：

```text
Python 发送高级命令；
PX4 内部负责具体飞控算法；
Gazebo 显示仿真结果。
```

---

## 12. 当前项目的简化与不足

当前项目仍然比较基础，主要用于理解 MAVSDK Action 和 telemetry 记录。

简化点包括：

```text
1. 只在 PX4 SITL 中测试，没有连接真实无人机
2. 只使用 Action 高级命令，没有使用 Offboard 控制
3. 起飞高度固定为 3 m
4. 悬停时间固定为 10 s
5. 没有加入复杂任务逻辑
6. 没有对 GPS / EKF / battery 做完整安全检查
7. 没有对异常情况做复杂恢复
8. 还没有对起飞降落 CSV 画专门的分析图
```

---

## 13. 后续改进方向

后续可以继续扩展：

```text
1. 对 takeoff_hover_land_telemetry.csv 画高度曲线
2. 对起飞、悬停、降落阶段分别分析
3. 增加 battery、velocity、health telemetry
4. 增加更完整的异常处理
5. 实现自动降落后 disarm 检查
6. 学习 Offboard 控制
7. 发送位置 setpoint
8. 实现简单轨迹飞行
9. 记录 Offboard 控制全过程 CSV
10. 对比 Action 控制和 Offboard 控制的区别
```

---

## 14. 项目总结

本项目完成了 MAVSDK Action 控制 PX4 SITL 的基础流程。

已完成能力：

```text
连接 PX4 SITL
读取 telemetry
自动 arm
自动 takeoff
自动 hover
自动 land
全过程保存 CSV
```

最重要的结论：

```text
Action 是发命令；
Telemetry 是看状态；
CSV 是保存过程；
曲线是分析结果。
```

一句话总结：

```text
本项目实现了用 Python 程序通过 MAVSDK 控制 PX4 SITL 完成一次自动起飞、悬停、降落，并记录全过程 telemetry。
```
