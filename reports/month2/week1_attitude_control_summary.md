# 第 2 个月第 1 周总结：姿态 PID 与级联控制入门

## 一、本周学习目标

本周的主要目标是从之前已经完成的高度 PID 控制，进一步过渡到四旋翼姿态控制。

之前的高度 PID 主要解决的是：

```text
高度误差 → PID → 推力 → 加速度 → 速度 → 高度
```

本周开始学习姿态控制，主要解决的是：

```text
姿态角误差 → PID → 力矩 → 角加速度 → 角速度 → 姿态角
```

本周重点包括：

1. 整理已有 PID 和四旋翼基础成果；
2. 完成 roll 单轴姿态 PID 仿真；
3. 完成 pitch 单轴姿态 PID 仿真；
4. 理解角速度控制；
5. 理解级联控制；
6. 将 roll / pitch 仿真整理成 README。

---

## 二、本周完成内容

### 1. 整理已有 PID 和四旋翼基础成果

本周首先整理了前期已经完成的内容，包括：

```text
PX4 SITL / Gazebo 仿真运行
高度 PID 控制实验
四旋翼基本结构
电机、桨叶、推力、力矩关系
roll / pitch / yaw 姿态角
PX4 数据流初步理解
```

通过整理，我确认后续不需要再重复从零做高度 PID，而应该从高度控制升级到姿态控制、角速度控制和 PX4 控制链路。

---

### 2. 完成 roll 单轴姿态 PID 仿真

完成了 roll 横滚角的单轴姿态 PID 仿真。

实验目标：

```text
目标 roll：10°
初始 roll：0°
PID 输出：roll 力矩
```

控制链路：

```text
目标 roll
    ↓
当前 roll
    ↓
roll 角度误差
    ↓
PID 控制器
    ↓
roll 力矩
    ↓
roll 角加速度
    ↓
roll 角速度
    ↓
roll 角度
```

通过这个实验，我理解了：

```text
高度 PID 输出的是推力；
roll 姿态 PID 输出的是力矩。
```

roll 控制在真实四旋翼中主要对应左右两侧电机的推力差，影响无人机左右倾斜和左右方向运动。

---

### 3. 完成 pitch 单轴姿态 PID 仿真

完成了 pitch 俯仰角的单轴姿态 PID 仿真。

实验目标：

```text
目标 pitch：-10°
初始 pitch：0°
PID 输出：pitch 力矩
```

控制链路：

```text
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
pitch 角加速度
    ↓
pitch 角速度
    ↓
pitch 角度
```

通过这个实验，我理解了：

```text
roll 控制左右倾斜；
pitch 控制前后俯仰。
```

pitch 控制在真实四旋翼中主要对应前后两侧电机的推力差。无人机向前飞时，通常需要机头下俯，使总推力方向向前倾斜，从而产生向前的水平分力。

---

### 4. 理解角速度控制

本周学习了姿态角、角速度和力矩之间的关系。

三个概念的区别：

```text
姿态角：当前已经转到什么角度
角速度：当前正在以多快速度旋转
力矩：让角速度发生变化的旋转作用
```

真实飞控通常不是直接：

```text
姿态角误差 → 电机输出
```

而是：

```text
姿态角误差
    ↓
期望角速度
    ↓
角速度误差
    ↓
力矩
    ↓
电机输出
```

也就是说：

```text
姿态环负责决定“应该转多快”；
角速度环负责决定“需要多大力矩”。
```

这为后续理解 PX4 中的 `vehicle_attitude_setpoint`、`vehicle_rates_setpoint`、`vehicle_torque_setpoint` 打下了基础。

---

### 5. 理解级联控制

本周学习了飞控中的级联控制。

级联控制的核心思想是：

```text
把一个高层目标，一层层转换成底层电机输出。
```

完整链路可以理解为：

```text
位置误差
    ↓
速度期望
    ↓
加速度 / 推力期望
    ↓
姿态期望
    ↓
角速度期望
    ↓
力矩 / 推力
    ↓
Control Allocation
    ↓
电机输出
```

各层作用：

```text
位置环：决定往哪里飞
速度环：决定怎么加速
姿态环：决定怎么倾斜
角速度环：决定需要多少力矩
控制分配：决定每个电机转多快
```

这个结构让我理解到：四旋翼飞控不是一个单独的 PID，而是一套多层嵌套的控制系统。

---

### 6. 整理 roll / pitch 仿真 README

本周将 roll / pitch 单轴姿态 PID 仿真整理成了 README。

README 中包括：

```text
项目目标
目录结构
核心文件说明
roll / pitch 的物理意义
编译方法
运行方法
绘图方法
实验结果观察方法
PID 参数理解
当前模型的简化与不足
后续改进方向
```

这一步的意义是把“能运行的代码”整理成“别人能看懂、自己以后能复现的项目”。

---

## 三、本周项目文件

本周主要项目路径：

```text
code/02_attitude_pid_sim/
```

主要文件：

```text
include/PIDController.hpp
src/PIDController.cpp
src/roll_pid_sim.cpp
src/pitch_pid_sim.cpp
scripts/plot_roll_pid.py
scripts/plot_pitch_pid.py
README.md
```

生成的数据和图像：

```text
data/roll_pid.csv
data/pitch_pid.csv

plots/roll_pid_angle.png
plots/roll_pid_rate.png
plots/roll_pid_torque.png

plots/pitch_pid_angle.png
plots/pitch_pid_rate.png
plots/pitch_pid_torque.png
```

本周笔记：

```text
notes/control/day32_roll_pid.md
notes/control/day33_pitch_pid.md
notes/control/day34_rate_control_basic.md
notes/control/day35_cascade_control.md
```

---

## 四、本周最重要的理解

### 1. 高度控制和姿态控制的区别

高度控制：

```text
高度误差 → PID → 推力
```

姿态控制：

```text
姿态角误差 → PID → 力矩
```

高度控制主要影响无人机上升、下降和悬停。

姿态控制主要影响无人机倾斜、转向和水平运动。

---

### 2. 推力和力矩的区别

推力主要让无人机产生平移运动。

例如：

```text
总推力大于重力 → 无人机上升
总推力等于重力 → 无人机悬停
总推力小于重力 → 无人机下降
```

力矩主要让无人机产生旋转运动。

例如：

```text
roll 力矩 → 左右横滚
pitch 力矩 → 前后俯仰
yaw 力矩 → 机头偏航
```

---

### 3. 为什么需要姿态环和角速度环

如果只根据姿态角误差直接输出力矩，无人机可能会转得太猛，容易超调和震荡。

加入角速度环后，飞控可以进一步判断：

```text
现在转得太快还是太慢？
接近目标时是否需要减速？
是否需要反向力矩抑制震荡？
```

因此，姿态环和角速度环配合可以让姿态控制更加稳定。

---

### 4. 为什么四旋翼控制是级联系统

四旋翼的任务目标通常是高层目标，例如：

```text
飞到某个位置
保持某个高度
沿航点飞行
悬停抗风
```

但电机只能执行底层命令：

```text
某个电机转快一点
某个电机转慢一点
```

所以飞控必须把高层目标一层层转换成底层电机输出。

这就是级联控制。

---

### 5. 当前仿真和真实 PX4 控制器的差距

当前 roll / pitch 仿真是简化模型，主要用于理解姿态 PID 的基本逻辑。

简化点包括：

```text
只考虑单轴运动
不考虑 roll、pitch、yaw 耦合
不考虑电机响应延迟
不考虑空气阻力
不考虑传感器噪声
不考虑控制分配
不考虑真实 PX4 中的姿态环和角速度环分离
```

真实 PX4 控制链路更接近：

```text
vehicle_attitude_setpoint
    ↓
Attitude Controller
    ↓
vehicle_rates_setpoint
    ↓
Rate Controller
    ↓
vehicle_torque_setpoint
    ↓
Control Allocation
    ↓
actuator_motors
```

---

## 五、本周存在的问题

目前还存在以下问题：

1. roll / pitch 仿真仍然是单轴模型，和真实四旋翼差距较大；
2. PID 参数目前主要靠手动尝试，还没有系统调参方法；
3. 还没有实现真正的姿态环 + 角速度环两层控制；
4. 还没有接入 PX4 SITL 的真实 telemetry 数据；
5. 还没有用 MAVSDK 控制 PX4 起飞、悬停和降落；
6. 对 PX4 姿态控制源码还没有深入阅读。

---

## 六、下周计划

下一周重点从“本地姿态控制仿真”转向“PX4 数据读取”。

计划学习内容：

```text
MAVLink 基本概念
MAVSDK 基本使用
PX4 SITL MAVLink 端口理解
MAVSDK 连接 PX4 SITL
读取 telemetry 数据
保存高度、位置、姿态、飞行模式到 CSV
绘制 PX4 telemetry 曲线
```

下周目标：

```text
用自己写的程序读取 PX4 SITL 中的无人机状态。
```

对应项目目录：

```text
code/03_mavsdk_telemetry/
```

---

## 七、本周总结

本周完成了从高度 PID 到姿态 PID 的过渡，理解了 roll 和 pitch 单轴姿态控制的基本逻辑，并进一步学习了角速度控制和级联控制。

本周最重要的收获是：

```text
姿态控制不是直接控制电机，而是通过姿态误差生成角速度或力矩需求，再经过控制分配变成电机输出。
```

一句话总结：

```text
本周完成了姿态控制入门：从 roll / pitch 单轴 PID 出发，理解了姿态角、角速度、力矩和级联控制之间的关系。
```
