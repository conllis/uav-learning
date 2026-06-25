# uav_mavsdk_bridge

## 项目目标

本项目用于将 PX4 SITL 的 MAVSDK telemetry 和 MAVSDK Action 控制能力接入 ROS2。

当前项目实现了三个基础功能：

1. 使用 MAVSDK 读取 PX4 telemetry。
2. 将 PX4 telemetry 发布成 ROS2 topic。
3. 通过 ROS2 topic 触发 MAVSDK Action，例如状态检查、起飞和降落。

本项目是第三个月核心项目 `PX4 SITL + MAVSDK + ROS2 外部控制与日志分析 Demo` 的第二周成果。

---

## 系统结构

```text
PX4 SITL
    ↓
MAVSDK
    ↓
ROS2 nodes
    ↓
Telemetry topic / Command topic / CSV logger
```

---

## 节点列表

### 1. px4_telemetry_bridge

功能：

* 连接 PX4 SITL
* 读取 relative altitude
* 读取 roll / pitch / yaw
* 读取 flight mode
* 发布成 ROS2 topic

运行：

```bash
ros2 run uav_mavsdk_bridge px4_telemetry_bridge
```

### 2. px4_telemetry_logger

功能：

* 订阅 PX4 telemetry topic
* 保存 CSV 文件

运行：

```bash
ros2 run uav_mavsdk_bridge px4_telemetry_logger
```

CSV 输出：

```text
~/uav-learning/data/month3/ros2_px4_telemetry.csv
```

### 3. px4_action_command_node

功能：

* 订阅 `/uav/action_command`
* 收到 `status` 时打印 PX4 状态
* 收到 `takeoff` 时调用 MAVSDK Action 起飞
* 收到 `land` 时调用 MAVSDK Action 降落

运行：

```bash
ros2 run uav_mavsdk_bridge px4_action_command_node
```

---

## Topic 列表

### Telemetry topics

| Topic                    | Message                | Description |
| ------------------------ | ---------------------- | ----------- |
| `/px4/relative_altitude` | `std_msgs/msg/Float32` | PX4 相对高度    |
| `/px4/roll`              | `std_msgs/msg/Float32` | 横滚角         |
| `/px4/pitch`             | `std_msgs/msg/Float32` | 俯仰角         |
| `/px4/yaw`               | `std_msgs/msg/Float32` | 偏航角         |
| `/px4/flight_mode`       | `std_msgs/msg/String`  | PX4 飞行模式    |

### Command topic

| Topic                 | Message               | Commands                    |
| --------------------- | --------------------- | --------------------------- |
| `/uav/action_command` | `std_msgs/msg/String` | `status`, `takeoff`, `land` |

---

## 运行步骤

### 1. 启动 PX4 SITL

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

### 2. 启动 telemetry bridge

```bash
cd ~/uav-learning/ros2_ws
source /opt/ros/humble/setup.bash
source install/setup.bash
ros2 run uav_mavsdk_bridge px4_telemetry_bridge
```

### 3. 查看 telemetry topic

```bash
ros2 topic list
ros2 topic echo /px4/relative_altitude
```

### 4. 启动 CSV logger

```bash
ros2 run uav_mavsdk_bridge px4_telemetry_logger
```

### 5. 启动 action command node

```bash
ros2 run uav_mavsdk_bridge px4_action_command_node
```

### 6. 发送命令

```bash
ros2 topic pub --once /uav/action_command std_msgs/msg/String "{data: 'status'}"
ros2 topic pub --once /uav/action_command std_msgs/msg/String "{data: 'takeoff'}"
ros2 topic pub --once /uav/action_command std_msgs/msg/String "{data: 'land'}"
```

---

## 安全注意事项

1. 当前项目只用于 PX4 SITL 仿真。
2. 起飞前必须确认 PX4 health 检查通过。
3. `land` 命令应随时可用。
4. 不要在真实飞机上直接运行未经验证的 Action 或 Offboard 控制代码。
5. 后续接入 Offboard 前，应先保证 telemetry 记录和降落逻辑稳定。

---

## 当前不足

1. 当前只实现 Action 控制，还没有实现 Offboard setpoint 控制。
2. 当前 CSV 只记录高度、姿态和飞行模式，还没有记录 local position。
3. 当前 command topic 只支持 `status`、`takeoff`、`land`。
4. 当前 bridge 使用 MAVSDK，不是 PX4 ROS2 uXRCE-DDS 原生桥接。
5. 还没有绘制 telemetry 曲线。

---

## 下一步计划

1. 增加 local position 记录。
2. 完成 Offboard hover。
3. 完成 Offboard move to point。
4. 完成 Offboard square trajectory。
5. 记录飞行全过程 CSV。
6. 绘制高度、姿态和任务阶段曲线。
