# Day 24 学习姿态角 roll、pitch、yaw

## 今日目标

理解四旋翼姿态角 roll、pitch、yaw 的含义，以及它们如何影响无人机运动。

---

## 1. 机体坐标系

常见机体坐标系可以理解为 FRD：

```text
X：Forward，机头前方
Y：Right，机体右方
Z：Down，机体下方
2. roll 横滚

roll 是绕机体 X 轴旋转。

直观理解：

无人机左右歪

作用：

主要影响左右方向运动
3. pitch 俯仰

pitch 是绕机体 Y 轴旋转。

直观理解：

机头上仰或下俯

作用：

主要影响前后方向运动
4. yaw 偏航

yaw 是绕机体 Z 轴旋转。

直观理解：

机头向左或向右转

作用：

主要改变机头朝向
5. 姿态角和运动关系
roll 改变左右倾斜
pitch 改变前后倾斜
yaw 改变机头朝向
throttle 改变总推力

当 roll 或 pitch 不为 0 时：

总推力方向倾斜
↓
产生水平分力
↓
无人机前后或左右运动
6. 姿态角和角速度区别
姿态角：当前已经转到什么角度
角速度：正在以多快速度旋转

示例：

roll = 10° 表示当前横滚角为 10°
roll_rate = 30°/s 表示横滚角速度为每秒 30°
7. 欧拉角和四元数

roll、pitch、yaw 属于欧拉角，直观但有局限。

飞控内部常用四元数表示姿态，因为四元数更适合连续旋转计算，也能避免欧拉角的万向节锁问题。

通常：

飞控内部：四元数
显示给人：roll / pitch / yaw
8. PX4 中观察姿态

启动仿真：

cd ~/PX4-Autopilot
make px4_sitl gz_x500

查看姿态：

listener vehicle_attitude 1

查看角速度：

listener vehicle_angular_velocity 1

查看期望姿态：

listener vehicle_attitude_setpoint 1
9. Day 24 C++ 实验

项目路径：

code/cpp/day24_attitude_rpy

编译运行：

cd ~/uav-learning/code/cpp/day24_attitude_rpy
cmake -S . -B build
cmake --build build
./build/day24_attitude_rpy

实验内容：

设置 roll / pitch / yaw
生成旋转矩阵
观察推力方向如何变化
10. 今日总结

今天理解了 roll、pitch、yaw 的基本含义。

最重要的结论：

roll 控制左右倾斜
pitch 控制前后倾斜
yaw 控制机头方向
roll / pitch 会让总推力方向倾斜，从而产生水平运动
yaw 主要改变朝向，不直接产生前后左右平移

---

# 十一、提交 Day 24
