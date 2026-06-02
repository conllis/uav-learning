# Day 27 整理 PX4 数据流

## 今日目标

理解 PX4 中数据如何从传感器流向状态估计、控制器、控制分配，最后变成电机输出。

---

## 1. PX4 数据流总览

PX4 内部大量模块通过 uORB topic 通信。

可以理解为：

```text
模块发布 topic
其他模块订阅 topic

主数据流：

传感器 / Gazebo 仿真数据
    ↓
uORB sensor topics
    ↓
EKF2 状态估计
    ↓
姿态 / 位置 / 速度估计
    ↓
位置控制器
    ↓
姿态控制器
    ↓
角速度控制器
    ↓
控制分配
    ↓
电机输出
2. 传感器数据

常见 topic：

sensor_accel
sensor_gyro
sensor_gps
sensor_baro
vehicle_imu

这些数据来自真实传感器或 Gazebo 仿真模型。

3. 状态估计数据

EKF2 读取传感器数据，输出无人机当前状态。

常见 topic：

vehicle_attitude
vehicle_local_position
vehicle_global_position
estimator_status

理解：

IMU / GPS / 气压计
    ↓
EKF2
    ↓
无人机姿态、位置、速度估计
4. 飞行状态和控制模式

commander 负责飞行器状态、解锁状态、飞行模式等。

常见 topic：

vehicle_status
vehicle_control_mode
vehicle_command

理解：

地面站 / 遥控器 / MAVLink 命令
    ↓
commander
    ↓
当前飞行模式、控制模式、解锁状态
5. 控制器数据流

多旋翼控制可以简化理解为：

目标位置
    ↓
位置控制器
    ↓
目标姿态 + 推力
    ↓
姿态控制器
    ↓
目标角速度
    ↓
角速度控制器
    ↓
力矩 / 推力

常见 topic：

trajectory_setpoint
vehicle_attitude_setpoint
vehicle_rates_setpoint
vehicle_thrust_setpoint
vehicle_torque_setpoint
6. 电机输出数据

控制分配负责把总推力、roll、pitch、yaw 力矩分配给具体电机。

常见 topic：

actuator_motors
actuator_outputs

理解：

总推力 + 三轴力矩
    ↓
Control Allocation
    ↓
每个电机的输出
7. 今天使用过的 PX4 命令
uorb top
listener sensor_accel
listener sensor_gyro
listener vehicle_attitude
listener vehicle_local_position
listener vehicle_status
listener vehicle_control_mode
listener trajectory_setpoint
listener actuator_motors
8. 今日总结

今天理解了 PX4 的核心数据流：

传感器
    ↓
uORB
    ↓
EKF2 状态估计
    ↓
位置 / 姿态 / 角速度控制
    ↓
Control Allocation
    ↓
actuator_motors
    ↓
电机输出

最重要的结论：

PX4 不是一个单一程序，而是很多模块通过 uORB topic 组成的实时飞控系统。

以后读源码时，不要一上来钻进函数细节，而要先问：

这个模块订阅了哪些 topic？
这个模块发布了哪些 topic？
它在整条飞控数据流中处于哪一层？

---

## 六、可选：查看日志系统

PX4 的 logger 可以记录 uORB topic，日志格式是 ULog；默认情况下，日志通常在解锁后开始记录、上锁后停止，也可以用 `logger status` 查看状态，用 `logger on` 手动开启。:contentReference[oaicite:6]{index=6}

你可以在 `pxh>` 里试一下：

```bash
logger status
logger on
logger status

今天先知道它的作用即可，不必深入分析 .ulg 文件。
