# Day 11 了解 PX4 飞行模式

## 今日目标

理解 PX4 中常见飞行模式的含义，并在 PX4 SITL + Gazebo 中观察模式变化。

---

## 1. 飞行模式是什么？

飞行模式表示 PX4 当前按照哪种规则控制无人机。

不同模式下，人、PX4 自动驾驶仪、外部程序的控制权不同。

---

## 2. 常见模式

### Stabilized 自稳模式

PX4 帮助保持姿态稳定，但不保持高度和位置。

### Altitude 定高模式

PX4 帮助保持高度，但不保持水平位置。

### Position 定点模式

PX4 帮助保持位置和高度，摇杆回中时无人机会悬停。

### Hold 保持模式

PX4 自动让无人机在当前位置悬停。

### Mission 任务模式

PX4 按照 QGroundControl 上传的航点任务自动飞行。

### Return 返航模式

PX4 自动返回 Home 点或安全位置。

### Land 降落模式

PX4 自动降落。

### Offboard 外部控制模式

外部程序持续发送 setpoint，PX4 按外部指令飞行。

---

## 3. 模式分类

```text
手动 / 半自动：
Stabilized
Altitude
Position

自动：
Takeoff
Hold
Mission
Return
Land

外部程序控制：
Offboard
4. 查看当前状态
commander status
listener vehicle_status 1

重点看：

arming_state
nav_state
failsafe
5. 今日实验流程
cd ~/PX4-Autopilot
make px4_sitl gz_x500

进入 pxh 后：

commander status
listener vehicle_status 1

commander arm
commander takeoff

commander mode hold
commander status
listener vehicle_status 1

commander land
commander disarm
shutdown
6. 常见提示
Mission rejected: empty

说明当前没有上传航点任务。

No connection to the GCS

说明没有连接 QGroundControl。

ekf2 missing data

说明 EKF 数据暂时不完整，刚启动时可能出现。

今日总结

今天理解了 PX4 飞行模式的基本分类。

最重要的模式：

Position：定点模式
Hold：悬停保持
Mission：航点任务
Return：返航
Land：自动降落
Offboard：外部程序控制

后续做 MAVSDK / ROS 2 控制时，Offboard 是重点。


保存：

```text
Ctrl + O
回车
Ctrl + X# Day 11 了解 PX4 飞行模式

## 今日目标

理解 PX4 中常见飞行模式的含义，并在 PX4 SITL + Gazebo 中观察模式变化。

---

## 1. 飞行模式是什么？

飞行模式表示 PX4 当前按照哪种规则控制无人机。

不同模式下，人、PX4 自动驾驶仪、外部程序的控制权不同。

---

## 2. 常见模式

### Stabilized 自稳模式

PX4 帮助保持姿态稳定，但不保持高度和位置。

### Altitude 定高模式

PX4 帮助保持高度，但不保持水平位置。

### Position 定点模式

PX4 帮助保持位置和高度，摇杆回中时无人机会悬停。

### Hold 保持模式

PX4 自动让无人机在当前位置悬停。

### Mission 任务模式

PX4 按照 QGroundControl 上传的航点任务自动飞行。

### Return 返航模式

PX4 自动返回 Home 点或安全位置。

### Land 降落模式

PX4 自动降落。

### Offboard 外部控制模式

外部程序持续发送 setpoint，PX4 按外部指令飞行。

---

## 3. 模式分类

```text
手动 / 半自动：
Stabilized
Altitude
Position

自动：
Takeoff
Hold
Mission
Return
Land

外部程序控制：
Offboard
