# Day 52 Offboard 最小实验准备

## 今日目标

今天开始进行 MAVSDK Offboard 最小实验，目标是先完成 Offboard 悬停，再尝试 Offboard 移动到一个点。

---

## 1. Offboard 最小实验思路

今天不直接用 Offboard 从地面起飞，而是采用更安全的流程：

```text
Action 起飞
    ↓
Offboard 接管
    ↓
Offboard 悬停或移动
    ↓
Offboard 停止
    ↓
Action 降落
```

这样可以降低实验难度。

---

## 2. 今日完成的程序

本次创建两个程序：

```text
code/03_mavsdk_telemetry/offboard_hover.py
code/03_mavsdk_telemetry/offboard_move_point.py
```

其中：

```text
offboard_hover.py：尝试进入 Offboard 并在 3 m 高度悬停
offboard_move_point.py：尝试进入 Offboard 后移动到一个点
```

---

## 3. Offboard 基本规则

Offboard 的核心规则：

```text
进入 Offboard 前，必须先发送一个 setpoint。
```

例如：

```python
await drone.offboard.set_position_ned(
    PositionNedYaw(0.0, 0.0, -3.0, 0.0)
)

await drone.offboard.start()
```

如果没有先发送 setpoint，PX4 可能拒绝进入 Offboard。

---

## 4. NED 坐标系

Offboard 位置控制使用 NED 坐标系。

NED 表示：

```text
N = North，北
E = East，东
D = Down，下
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

## 5. Offboard 悬停实验

悬停 setpoint：

```python
PositionNedYaw(0.0, 0.0, -3.0, 0.0)
```

含义：

```text
x = 0 m
y = 0 m
z = -3 m
yaw = 0°
```

也就是在本地原点上方 3 m 悬停。

---

## 6. Offboard 移动到一个点

移动目标点：

```python
PositionNedYaw(3.0, 0.0, -3.0, 0.0)
```

含义：

```text
x = 3 m
y = 0 m
z = -3 m
yaw = 0°
```

也就是在 3 m 高度，向北移动 3 m。

---

## 7. Action 和 Offboard 的配合

今天的流程中：

```text
Action 负责起飞和降落；
Offboard 负责悬停和移动。
```

具体流程：

```text
arm
takeoff
set initial offboard setpoint
start offboard
send hover or move setpoint
stop offboard
land
```

---

## 8. 今日理解

今天理解了：

```text
Offboard 不是高级动作命令，而是持续目标控制；
setpoint 是外部程序发给 PX4 的控制目标；
Offboard 进入前必须先发送 setpoint；
NED 坐标系中 z 向下为正，所以 z=-3 表示向上 3 m；
Action 和 Offboard 可以配合使用。
```

---

## 9. 实验结果记录

Offboard 悬停是否成功：

```text
是 / 否：
```

Offboard 移动是否成功：

```text
是 / 否：
```

悬停高度：

```text
____ m
```

移动目标点：

```text
x = ____ m
y = ____ m
z = ____ m
```

是否正常降落：

```text
是 / 否：
```

---

## 10. 今日总结

今天完成了 Offboard 最小实验准备，并尝试使用位置 setpoint 进行悬停和移动。

最重要的结论：

```text
Offboard 的核心是持续给 PX4 发送 setpoint，而不是直接控制电机。
```

一句话总结：

```text
Day 52 的核心是从 Action 高级动作控制，进入 Offboard 位置目标控制。
```
