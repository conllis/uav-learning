# Day 26 看 PX4 中的位置、速度、姿态数据

## 今日目标

学习使用 PX4 shell 中的 `listener` 命令查看 PX4 内部 uORB 数据，包括位置、速度、姿态和角速度。

---

## 1. 启动 PX4 SITL

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500

进入 PX4 shell：

pxh>
2. uORB 和 listener

PX4 内部模块通过 uORB topic 交换数据。

listener 可以查看某个 topic 的当前数据。

示例：

listener vehicle_local_position 1
3. 查看本地位置和速度
listener vehicle_local_position 1

重点字段：

x：NED 北向位置
y：NED 东向位置
z：NED 下向位置
vx：北向速度
vy：东向速度
vz：下向速度
heading：航向角
xy_valid：水平位置是否有效
z_valid：高度是否有效

PX4 本地位置常用 NED 坐标系：

X：North，北
Y：East，东
Z：Down，下

因此：

无人机上升时，z 通常变成负数
无人机向上速度时，vz 通常为负
4. 查看全局位置
listener vehicle_global_position 1

重点字段：

lat：纬度
lon：经度
alt：高度
vel_n：北向速度
vel_e：东向速度
vel_d：下向速度
5. 查看姿态
listener vehicle_attitude 1

重点字段：

q：四元数姿态

PX4 内部常用四元数表示姿态，界面上通常转换成 roll / pitch / yaw 显示。

6. 查看角速度
listener vehicle_angular_velocity 1

角速度表示无人机正在绕机体轴旋转的速度。

x 轴角速度：roll rate
y 轴角速度：pitch rate
z 轴角速度：yaw rate
7. 查看飞行器状态
listener vehicle_status 1

或者：

commander status

重点字段：

arming_state：解锁状态
nav_state：导航 / 飞行模式
failsafe：是否故障保护
vehicle_type：飞行器类型
8. 今日观察流程
listener vehicle_status 1
listener vehicle_local_position 1
listener vehicle_attitude 1
listener vehicle_angular_velocity 1

commander arm
commander takeoff

listener vehicle_local_position 1
listener vehicle_attitude 1
listener vehicle_angular_velocity 1

commander land
commander disarm
shutdown
9. 今日理解

位置和速度：

x, y, z 表示在哪里
vx, vy, vz 表示往哪里运动

姿态和角速度：

vehicle_attitude 表示当前姿态
vehicle_angular_velocity 表示当前旋转速度

PX4 中很多控制器都是在比较：

当前状态
↓
期望状态
↓
误差
↓
控制输出

这和 PID 控制思想是一致的。

今日总结

今天学习了如何在 PX4 中查看位置、速度、姿态和角速度数据。

最重要的结论：

PX4 常用 NED 坐标系，z 向下为正；无人机上升时，local position 的 z 和 vz 通常为负。

---

# 十五、提交 Day 26
