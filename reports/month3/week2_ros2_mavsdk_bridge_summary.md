# 第 3 个月第 2 周总结：ROS2 + MAVSDK 桥接

## 1. 本周目标

本周目标是把 PX4 SITL、MAVSDK 和 ROS2 连接起来，完成一个基础桥接系统：

```text
PX4 SITL
    ↓
MAVSDK
    ↓
ROS2 topic
    ↓
Logger / Command Node
```

本周重点不是单独学习 ROS2 或 MAVSDK，而是让 ROS2 能组织 PX4 的 telemetry 数据和 Action 控制命令。

---

## 2. 本周完成内容

### 2.1 创建 uav_mavsdk_bridge 包

创建了 ROS2 Python package：

```text
uav_mavsdk_bridge
```

该包用于存放 MAVSDK 与 ROS2 桥接相关节点。

---

### 2.2 MAVSDK telemetry 转 ROS2 topic

完成节点：

```text
px4_telemetry_bridge.py
```

该节点使用 MAVSDK 连接 PX4 SITL，并读取：

* relative altitude
* roll
* pitch
* yaw
* flight mode

然后发布成 ROS2 topic：

```text
/px4/relative_altitude
/px4/roll
/px4/pitch
/px4/yaw
/px4/flight_mode
```

---

### 2.3 ROS2 telemetry logger 保存 CSV

完成节点：

```text
px4_telemetry_logger.py
```

该节点订阅 PX4 telemetry topic，并保存 CSV 文件：

```text
~/uav-learning/data/month3/ros2_px4_telemetry.csv
```

CSV 字段包括：

```text
time_sec, relative_altitude_m, roll_deg, pitch_deg, yaw_deg, flight_mode
```

---

### 2.4 ROS2 topic 触发 MAVSDK Action

完成节点：

```text
px4_action_command_node.py
```

该节点订阅：

```text
/uav/action_command
```

支持命令：

```text
status
takeoff
land
```

通过 ROS2 topic 可以触发 MAVSDK Action，从而完成 PX4 状态检查、起飞和降落。

---

## 3. 为什么要把 MAVSDK telemetry 发布成 ROS2 topic？

MAVSDK 可以直接读取 PX4 telemetry，但如果每个模块都直接连接 PX4，系统会变得混乱。

把 MAVSDK telemetry 发布成 ROS2 topic 后，其他节点只需要订阅 topic：

```text
PX4 SITL
    ↓
MAVSDK
    ↓
px4_telemetry_bridge
    ↓
ROS2 topic
    ↓
logger / controller / plotter
```

这样可以让系统解耦：

* bridge 负责读取 PX4
* logger 负责保存数据
* controller 负责生成控制命令
* plotter 负责离线分析

---

## 4. ROS2 command topic 和 MAVSDK Action 怎么结合？

ROS2 command topic 用来接收外部命令：

```text
/uav/action_command
```

例如：

```bash
ros2 topic pub --once /uav/action_command std_msgs/msg/String "{data: 'takeoff'}"
```

Action command node 收到命令后，根据字符串调用 MAVSDK Action：

```text
status  → 读取 PX4 telemetry 状态
takeoff → arm + takeoff
land    → land
```

这说明 ROS2 负责组织命令入口，MAVSDK 负责真正与 PX4 通信。

---

## 5. 这个桥接项目和 PX4 ROS2 Bridge / MAVROS 有什么关系？

当前项目是一个轻量级学习版 bridge：

```text
PX4 SITL → MAVSDK → ROS2 topic
```

它的优点是容易理解，适合学习 telemetry、Action 和 Offboard 的基本工程流程。

MAVROS 和 PX4 ROS2 Bridge 更接近正式工程方案：

* MAVROS：通过 MAVLink 把 PX4 与 ROS/ROS2 连接起来。
* PX4 ROS2 Bridge / uXRCE-DDS：更接近 PX4 原生 ROS2 通信方式，可以直接对接 PX4 uORB 相关数据。

当前项目不是为了替代 MAVROS 或 PX4 ROS2 Bridge，而是为了先掌握无人机系统桥接的基本思想。

---

## 6. 当前项目的不足

1. 当前只记录高度、姿态和飞行模式，还没有记录 local position。
2. 当前只支持 Action 控制，还没有实现 Offboard setpoint 控制。
3. 当前 command topic 使用字符串，后续可以改成更规范的 service 或 action。
4. 当前 CSV 还没有自动画图分析。
5. 当前没有完整异常处理和状态机，不适合直接用于真实无人机。

---

## 7. 本周最大收获

本周最大的收获是完成了从“ROS2 基础通信”到“ROS2 + PX4 telemetry 桥接”的升级。

第 1 周发布的是模拟数据：

```text
/uav/relative_altitude
/uav/roll
/uav/pitch
/uav/yaw
```

第 2 周发布的是 PX4 SITL 的真实 telemetry：

```text
/px4/relative_altitude
/px4/roll
/px4/pitch
/px4/yaw
/px4/flight_mode
```

这说明 ROS2 的 publisher/subscriber 机制已经可以服务于 PX4 飞控仿真系统。

---

## 8. 下周计划

第 3 周进入 Offboard 强化，目标是完成：

1. Offboard 问题记录与稳定流程整理。
2. Offboard 悬停稳定版。
3. Offboard 移动到一个点。
4. Offboard 方形轨迹。
5. 保存全过程 telemetry CSV。
6. 绘制高度、姿态和任务阶段曲线。

下周核心目标是：

```text
Action 起飞
    ↓
Offboard 接管
    ↓
发送 setpoint
    ↓
记录 telemetry
    ↓
Action 降落
```
