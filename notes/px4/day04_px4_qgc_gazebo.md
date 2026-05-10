# Day 04 了解 PX4、QGroundControl、Gazebo

## 今日目标

理解无人机仿真学习中的三个核心工具：

- PX4
- QGroundControl
- Gazebo

并理解它们之间的关系。

---

## 1. PX4 是什么？

PX4 是开源无人机飞控系统，可以运行在真实飞控硬件上，也可以在电脑上通过 SITL 方式运行。

PX4 主要负责：

- 读取传感器数据
- 状态估计
- 姿态控制
- 位置控制
- 飞行模式管理
- 电机控制输出
- MAVLink 通信
- 飞行日志记录

我可以把 PX4 理解为无人机的大脑。

---

## 2. SITL 是什么？

SITL 是 Software In The Loop，也就是软件在环仿真。

它的意思是：不需要真实飞控板和真实无人机，直接让 PX4 飞控程序运行在电脑中。

SITL 的优点：

- 安全
- 不需要真实飞机
- 不会炸机
- 方便调试
- 方便重复实验
- 适合学习飞控系统

---

## 3. QGroundControl 是什么？

QGroundControl 是无人机地面站软件。

它主要负责：

- 连接无人机
- 查看飞行状态
- 修改飞控参数
- 规划航点任务
- 控制起飞和降落
- 查看地图和轨迹
- 下载和查看日志

我可以把 QGroundControl 理解为地面站和控制界面。

---

## 4. Gazebo 是什么？

Gazebo 是机器人仿真器。

它主要负责模拟：

- 无人机模型
- 三维环境
- 物理运动
- 重力
- 碰撞
- IMU
- GPS
- 气压计
- 相机
- 激光雷达

我可以把 Gazebo 理解为虚拟飞行场地和虚拟无人机。

---

## 5. 三者关系

```text
QGroundControl
    ↑↓ MAVLink
PX4 SITL
    ↑↓ 仿真接口 / MAVLink
Gazebo
