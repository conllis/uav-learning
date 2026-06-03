# Day 33 pitch 单轴姿态 PID

## 今日目标

今天学习 pitch 单轴姿态 PID，把控制对象从 roll 横滚控制扩展到 pitch 俯仰控制。

---

## 1. pitch 是什么

pitch 是无人机绕机体左右轴的旋转。

直观理解：

```text
机头上仰
机头下俯

在四旋翼中，pitch 主要影响无人机前后方向运动。

2. pitch 控制的实际意义

如果无人机要向前飞，通常需要机头下俯。

过程可以理解为：

后侧电机推力增大
前侧电机推力减小
    ↓
机头下俯
    ↓
总推力方向向前倾斜
    ↓
产生向前的水平分力
    ↓
无人机向前飞
3. pitch PID 控制链路

pitch PID 的控制链路是：

目标 pitch
    ↓
当前 pitch
    ↓
pitch 角度误差
    ↓
PID 控制器
    ↓
pitch 力矩
    ↓
角加速度
    ↓
角速度
    ↓
pitch 角度
4. 和 roll PID 的区别

roll PID：

控制左右倾斜
主要对应左右两侧推力差

pitch PID：

控制前后俯仰
主要对应前后两侧推力差

二者数学形式类似，都是：

角度误差
    ↓
PID
    ↓
力矩
    ↓
角加速度
    ↓
角速度
    ↓
角度
5. 本次仿真模型

本次只考虑 pitch 单轴，不考虑 roll、yaw 和高度变化。

参数：

目标 pitch：-10°
初始 pitch：0°
仿真时间：5 s
时间步长：0.01 s

简化模型：

pitch 力矩 / 转动惯量 = pitch 角加速度
角加速度积分 = pitch 角速度
角速度积分 = pitch 角
6. 实验观察指标

需要观察：

是否接近目标 pitch
是否超调
是否震荡
响应是否过慢
力矩输出是否过大
7. PID 参数影响

P 项：

P 越大，响应越快
P 太大，容易超调和震荡

D 项：

D 可以抑制震荡
D 像阻尼，让姿态变化更平滑

I 项：

I 用于消除长期误差
在姿态入门仿真中可以先不加或少加
8. 今日总结

今天完成了 pitch 单轴姿态 PID 仿真。

最重要的理解是：

pitch PID 根据 pitch 角度误差输出 pitch 力矩。
pitch 力矩改变 pitch 角速度，pitch 角速度再改变 pitch 角。

roll 和 pitch PID 都属于姿态控制的基础。

后续要继续学习：

角速度控制
姿态环 + 角速度环
级联 PID
PX4 中 position control、attitude control、rate control 的关系
