# Day 50 准备 Offboard 控制概念

## 今日目标

今天学习 Offboard 控制的基本概念，理解 Offboard 和 Action 的区别，为后续使用 MAVSDK Python 实现位置控制和轨迹控制做准备。

---

## 1. 什么是 Offboard

Offboard 是一种外部控制模式。

在 Offboard 中，外部程序持续向 PX4 发送控制目标。

控制目标可以是：

```text
目标位置
目标速度
目标姿态
目标角速度
```

一句话理解：

```text
Offboard 是让外部程序持续给 PX4 发送 setpoint，让 PX4 按这些目标控制无人机。
```

---

## 2. Action 和 Offboard 的区别

Action 是高级动作命令。

例如：

```text
arm
takeoff
land
return_to_launch
```

Action 更像是告诉 PX4：

```text
请你起飞
请你降落
请你返航
```

Offboard 是持续控制目标。

例如：

```text
现在目标位置是 x=0, y=0, z=-3
现在目标速度是 vx=1, vy=0, vz=0
现在目标 yaw 是 90°
```

对比：

```text
Action：发送一次高级动作命令
Offboard：持续发送控制目标 setpoint
```

---

## 3. 什么是 setpoint

setpoint 是控制目标。

例如：

```text
目标高度：3 m
目标位置：x=0, y=0, z=-3
目标速度：向前 1 m/s
目标 yaw：90°
```

Offboard 发送的是 setpoint，不是电机转速。

PX4 接收到 setpoint 后，会由内部控制器完成真正的飞控计算。

---

## 4. 为什么要持续发送 setpoint

Offboard 模式下，PX4 需要确认外部控制器仍然正常工作。

如果外部程序停止发送 setpoint，PX4 会认为外部控制失效。

因此 Offboard 必须持续发送 setpoint。

这是一种安全机制。

可以理解为：

```text
外部程序不断发 setpoint，等于不断告诉 PX4：我还活着，控制目标还有效。
```

---

## 5. Offboard 和 PX4 内部控制器的关系

Offboard 不直接控制电机。

Offboard 程序提供目标：

```text
目标位置 / 目标速度 / 目标姿态
```

PX4 内部控制器负责实现目标：

```text
Position Controller
    ↓
Attitude Controller
    ↓
Rate Controller
    ↓
Control Allocation
    ↓
actuator_motors
```

完整链路：

```text
Python Offboard 程序
    ↓
MAVSDK
    ↓
MAVLink
    ↓
PX4 Offboard 模式
    ↓
PX4 控制器
    ↓
电机输出
```

---

## 6. Offboard 适合做什么

Offboard 适合更灵活的自主飞行任务：

```text
飞正方形轨迹
飞圆形轨迹
视觉引导飞行
避障控制
目标跟踪
外部路径规划
```

例如：

```text
外部视觉程序发现目标
    ↓
计算目标方向
    ↓
生成速度 setpoint
    ↓
通过 Offboard 发给 PX4
    ↓
PX4 控制无人机移动
```

---

## 7. Offboard 基本流程

后续程序通常按这个流程写：

```text
1. 连接 PX4
2. 等待 health ready
3. arm
4. takeoff 到安全高度
5. 先发送一个初始 setpoint
6. start Offboard
7. 持续发送 setpoint
8. 执行移动或轨迹
9. stop Offboard
10. land
```

其中最重要的是：

```text
进入 Offboard 前，必须先发送 setpoint。
```

---

## 8. 常见 setpoint 类型

常见 Offboard setpoint 包括：

```text
位置 setpoint
速度 setpoint
姿态 setpoint
角速度 setpoint
```

入门建议：

```text
先学位置 setpoint
再学速度 setpoint
最后再理解姿态和角速度 setpoint
```

---

## 9. NED 坐标系

Offboard 常用 NED 坐标系。

NED 表示：

```text
N：North，北
E：East，东
D：Down，下
```

坐标含义：

```text
x：向北为正
y：向东为正
z：向下为正
```

因此：

```text
z = -3
```

表示向上 3 米。

---

## 10. Offboard 和 Action 的配合

实际程序中，Action 和 Offboard 经常配合使用：

```text
Action arm
Action takeoff
Offboard start
Offboard 发送 setpoint
Offboard stop
Action land
```

可以理解为：

```text
起飞和降落交给 Action；
中间的移动和轨迹控制交给 Offboard。
```

---

## 11. 今日总结

今天理解了 Offboard 的基本概念。

最重要的结论：

```text
Action 是高级动作命令；
Offboard 是持续发送控制目标；
setpoint 是外部程序发给 PX4 的控制目标；
Offboard 必须持续发送 setpoint；
PX4 内部仍然负责真正的飞控控制。
```

一句话总结：

```text
Offboard 是从“让 PX4 自动起飞降落”进入“让外部程序控制飞行轨迹”的关键一步。
```
