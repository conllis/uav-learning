# 第 2 个月第 3 周总结：MAVSDK Action 控制入门

## 一、本周学习目标

本周的主要目标是从“读取 PX4 状态”升级到“用 Python 程序控制 PX4 SITL 飞行”。

上一周已经完成：

```text
连接 PX4 SITL
读取 telemetry
保存 telemetry 到 CSV
绘制 telemetry 曲线
```

本周进一步学习 MAVSDK Action，完成：

```text
理解 Action 控制
自动解锁
自动起飞
起飞后悬停
自动降落
边控制边记录 telemetry
整理 Action 控制 README
准备 Offboard 控制概念
```

本周最重要的主线是：

```text
Telemetry：看无人机状态
Action：给无人机发高级动作命令
CSV：记录飞行全过程
Offboard：下一阶段持续发送 setpoint 控制轨迹
```

---

## 二、本周完成内容

### 1. 学习 MAVSDK Action

本周首先学习了 MAVSDK Action 的基本概念。

Action 是 MAVSDK 中用于发送高级飞行动作命令的模块。

常见 Action 命令包括：

```text
arm
takeoff
land
return_to_launch
disarm
set_takeoff_altitude
```

本周理解到：

```text
Telemetry 是读取状态；
Action 是发送命令。
```

也就是：

```text
Telemetry：PX4 → Python
Action：Python → PX4
```

Action 不是直接控制电机，而是向 PX4 发送高级动作命令。真正的高度控制、姿态控制、角速度控制和电机分配，仍然由 PX4 内部完成。

---

### 2. 实现自动解锁 + 起飞

本周实现了第一个 Action 控制程序：

```text
code/03_mavsdk_telemetry/action_arm_takeoff.py
```

程序流程：

```text
连接 PX4 SITL
    ↓
等待连接成功
    ↓
等待 health ready
    ↓
设置起飞高度 3 m
    ↓
arm 解锁
    ↓
takeoff 起飞
    ↓
读取 relative_altitude_m
    ↓
判断是否接近目标高度
```

通过这个程序，我第一次用 Python 程序让 PX4 SITL 自动解锁并起飞。

核心理解：

```text
takeoff() 只是发送起飞命令；
是否真的起飞成功，需要通过 telemetry 判断。
```

因此，程序中必须读取：

```text
relative_altitude_m
```

观察高度是否从 0 m 上升到接近 3 m。

---

### 3. 实现起飞 + 悬停 + 降落

本周进一步实现完整基础飞行流程：

```text
code/03_mavsdk_telemetry/action_takeoff_hover_land.py
```

程序流程：

```text
arm
    ↓
takeoff
    ↓
hover
    ↓
land
```

也就是：

```text
解锁 → 起飞 → 悬停 → 降落
```

在这个程序中，Action 负责发送命令：

```text
arm()
takeoff()
land()
```

Telemetry 负责观察结果：

```text
relative_altitude_m 是否上升
relative_altitude_m 是否稳定
relative_altitude_m 是否下降
```

通过这个任务，我理解到：一个完整的飞行程序不能只发命令，还要持续读取无人机状态，确认每一步是否真的执行成功。

---

### 4. 边控制边记录 telemetry

本周完成了综合程序：

```text
code/03_mavsdk_telemetry/action_takeoff_hover_land_log.py
```

这个程序实现了：

```text
自动 arm
自动 takeoff
自动 hover
自动 land
全过程记录 telemetry 到 CSV
```

输出文件：

```text
code/03_mavsdk_telemetry/data/takeoff_hover_land_telemetry.csv
```

保存字段包括：

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

`mission_phase` 用来标记当前飞行阶段：

```text
init
set_takeoff_altitude
arming
takeoff
hover
landing
finished
```

这样后续画图时，可以清楚知道某段高度变化对应起飞、悬停还是降落。

---

### 5. 整理 Action 控制 README

本周将 MAVSDK Action 控制项目整理成了说明文档：

```text
code/03_mavsdk_telemetry/README_action_control.md
```

README 中说明了：

```text
项目目标
项目背景
目录结构
核心程序作用
运行方法
CSV 字段含义
mission_phase 含义
Action 和 Telemetry 的关系
当前不足
后续改进方向
```

这一步的意义是把“能运行的程序”整理成“别人能看懂、自己以后能复现的项目”。

---

### 6. 准备 Offboard 控制概念

本周最后学习了 Offboard 控制的基本概念。

Action 和 Offboard 的区别：

```text
Action：发送一次高级动作命令
Offboard：持续发送控制目标 setpoint
```

Action 适合：

```text
起飞
降落
返航
```

Offboard 适合：

```text
位置控制
速度控制
轨迹跟踪
视觉引导
避障
目标跟随
```

本周理解到，Offboard 不是直接控制电机，而是持续向 PX4 发送 setpoint，例如：

```text
目标位置
目标速度
目标姿态
目标角速度
```

PX4 内部仍然负责：

```text
位置控制
姿态控制
角速度控制
控制分配
电机输出
```

---

## 三、本周项目文件

本周主要项目目录：

```text
code/03_mavsdk_telemetry/
```

本周核心程序：

```text
action_status_check.py
action_arm_takeoff.py
action_takeoff_hover_land.py
action_takeoff_hover_land_log.py
README_action_control.md
```

本周输出数据：

```text
data/takeoff_hover_land_telemetry.csv
```

本周笔记：

```text
notes/mavlink/day45_mavsdk_action_basic.md
notes/mavlink/day46_mavsdk_arm_takeoff.md
notes/mavlink/day47_takeoff_hover_land.md
notes/mavlink/day48_control_and_log_telemetry.md
notes/offboard/day50_offboard_concept.md
```

本周 README：

```text
code/03_mavsdk_telemetry/README_action_control.md
```

---

## 四、本周最重要的理解

### 1. Telemetry 和 Action 的关系

本周最重要的一句话是：

```text
Action 发命令，Telemetry 看结果。
```

例如：

```python
await drone.action.takeoff()
```

这句话只是表示：

```text
向 PX4 发送起飞命令。
```

但它不代表无人机已经飞到目标高度。

真正判断起飞是否完成，要看：

```text
relative_altitude_m 是否上升到目标高度附近
```

同理：

```python
await drone.action.land()
```

只是发送降落命令。

是否降落完成，需要观察：

```text
relative_altitude_m 是否接近 0
flight_mode 是否变化
armed 状态是否变化
```

---

### 2. Action 不是直接控制电机

MAVSDK Action 并不是直接控制四个电机。

调用：

```python
await drone.action.takeoff()
```

实际链路是：

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
Python 负责发高级命令；
PX4 负责真正的飞控控制；
Gazebo 负责显示仿真结果。
```

---

### 3. 为什么要记录 CSV

如果只让无人机起飞、悬停、降落，只能看到现象。

保存 CSV 后，可以分析：

```text
起飞高度是否达到目标
悬停是否稳定
降落是否平滑
姿态角是否剧烈变化
飞行模式是否正确切换
```

因此，飞控实验不能只控制，还要记录数据。

本周建立了完整流程：

```text
Action 控制
    ↓
Telemetry 读取
    ↓
CSV 保存
    ↓
后续曲线分析
```

---

### 4. mission_phase 的意义

`mission_phase` 是本周新增的重要字段。

它用来标记任务阶段：

```text
takeoff
hover
landing
```

这样后续分析高度曲线时，可以知道：

```text
哪一段是起飞
哪一段是悬停
哪一段是降落
```

这让 telemetry 数据从单纯的数字，变成了可以对应任务阶段的飞行记录。

---

### 5. Offboard 是下一阶段重点

本周最后学习到：

```text
Action 是高级动作命令；
Offboard 是持续发送 setpoint。
```

Action 适合完成：

```text
起飞
降落
返航
```

Offboard 适合完成：

```text
移动到指定位置
按照速度飞行
执行轨迹
外部算法控制无人机
```

下一阶段会从 Action 进入 Offboard。

---

## 五、本周存在的问题

目前还存在以下问题：

```text
1. 目前只实现了 Action 控制，还没有实现 Offboard 控制；
2. 目前飞行任务比较简单，只是起飞、悬停、降落；
3. 起飞高度和悬停时间仍然是固定参数；
4. 还没有对 takeoff_hover_land_telemetry.csv 画专门曲线；
5. 异常处理还比较基础；
6. 还没有加入 battery、velocity、health 等更多 telemetry；
7. 还没有实现降落后自动确认 disarm；
8. 还没有让无人机按指定位置或轨迹移动。
```

---

## 六、下周计划

下周重点进入 Offboard 控制。

计划内容：

```text
1. 复习 Offboard 和 setpoint 概念
2. 理解 NED 坐标系
3. 实现 Offboard 悬停 setpoint
4. 实现 Offboard 向前移动一点
5. 保存 Offboard 控制全过程 telemetry
6. 绘制 Offboard 高度和位置曲线
7. 对比 Action 控制和 Offboard 控制
```

下周目标：

```text
用 Python 程序持续发送 setpoint，让 PX4 SITL 按外部目标移动。
```

---

## 七、本周总结

本周完成了 MAVSDK Action 控制入门。

从上一周的“读取 PX4 状态”，升级到了本周的“用 Python 控制 PX4 飞行”。

本周已经具备的能力：

```text
连接 PX4 SITL
读取 telemetry
自动 arm
自动 takeoff
自动 hover
自动 land
边控制边记录 telemetry
整理项目 README
理解 Offboard 基本概念
```

本周最重要的收获是：

```text
已经可以用 Python 程序通过 MAVSDK Action 控制 PX4 SITL 完成一次完整的自动起飞、悬停、降落，并记录全过程 telemetry。
```

一句话总结：

```text
本周完成了从“看 PX4 状态”到“控制 PX4 飞行”的过渡，为下一阶段 Offboard 外部控制打下基础。
```
