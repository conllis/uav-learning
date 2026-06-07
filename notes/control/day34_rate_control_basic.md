# Day 34 角速度控制理解

## 今日目标

今天学习角速度控制，理解姿态角、角速度和力矩之间的关系。

---

## 1. 姿态角是什么

姿态角表示无人机当前已经转到什么角度。

例如：

```text
roll = 10°
```

表示无人机当前横滚倾斜 10°。

姿态角回答的问题是：

```text
现在歪到什么角度了？
```

---

## 2. 角速度是什么

角速度表示无人机正在以多快的速度旋转。

例如：

```text
roll_rate = 30°/s
```

表示无人机正在以每秒 30° 的速度横滚。

角速度回答的问题是：

```text
现在转得快不快？
```

---

## 3. 力矩是什么

力矩是让物体产生旋转的作用。

对于无人机：

```text
roll 力矩让无人机绕 roll 轴旋转
pitch 力矩让无人机绕 pitch 轴旋转
yaw 力矩让无人机绕 yaw 轴旋转
```

力矩回答的问题是：

```text
我要施加多大的旋转力量？
```

---

## 4. 姿态控制和角速度控制的关系

真实飞控通常不是直接：

```text
姿态角误差
    ↓
电机输出
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
姿态控制器负责算“应该转多快”
角速度控制器负责算“需要多大力矩”
```

---

## 5. 为什么需要角速度控制

如果只根据角度误差直接输出力矩，无人机可能会转得太猛，容易超调和震荡。

加入角速度控制后，可以判断：

```text
现在是不是转得太快？
现在是不是转得太慢？
接近目标时要不要减速？
```

这样姿态控制会更稳定。

---

## 6. 姿态环和角速度环

姿态环：

```text
目标姿态角
    ↓
当前姿态角
    ↓
姿态角误差
    ↓
期望角速度
```

角速度环：

```text
期望角速度
    ↓
当前角速度
    ↓
角速度误差
    ↓
力矩输出
```

合起来：

```text
目标姿态角
    ↓
姿态环
    ↓
期望角速度
    ↓
角速度环
    ↓
力矩
    ↓
电机输出
```

---

## 7. roll / pitch / yaw 角速度

三个角速度可以理解为：

```text
roll_rate：横滚转得多快
pitch_rate：俯仰转得多快
yaw_rate：偏航转得多快
```

也常写成：

```text
p：roll rate
q：pitch rate
r：yaw rate
```

---

## 8. 和 PX4 数据流的关系

PX4 中可以这样理解：

```text
vehicle_attitude_setpoint
    ↓
姿态控制器
    ↓
vehicle_rates_setpoint
    ↓
角速度控制器
    ↓
vehicle_torque_setpoint
    ↓
Control Allocation
    ↓
actuator_motors
```

其中：

```text
vehicle_attitude_setpoint：目标姿态
vehicle_rates_setpoint：目标角速度
vehicle_torque_setpoint：目标力矩
actuator_motors：电机输出
```

---

## 9. PX4 中观察角速度

启动仿真：

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

查看当前姿态：

```bash
listener vehicle_attitude 1
```

查看当前角速度：

```bash
listener vehicle_angular_velocity 1
```

查看期望角速度：

```bash
listener vehicle_rates_setpoint 1
```

---

## 10. 今日总结

今天理解了姿态角、角速度和力矩之间的关系。

最重要的结论是：

```text
姿态角表示已经转到哪里；
角速度表示正在转得多快；
力矩决定角速度如何变化。
```

飞控中通常使用两层结构：

```text
姿态环：角度误差 → 期望角速度
角速度环：角速度误差 → 力矩
```

这为后续理解 PX4 姿态控制器和角速度控制器打基础。
