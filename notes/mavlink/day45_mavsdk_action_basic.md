# Day 45 学习 MAVSDK Action

## 今日目标

今天学习 MAVSDK Action 的基本概念，理解 Action 和 Telemetry 的区别，并为后续使用 Python 控制 PX4 SITL 起飞、悬停和降落做准备。

---

## 1. Action 是什么

Action 是 MAVSDK 中用于发送常见飞行动作命令的模块。

它可以向 PX4 发送高级动作命令，例如：

```text
arm
takeoff
land
return_to_launch
disarm
```

一句话理解：

```text
Telemetry 用来读取无人机状态，Action 用来让无人机执行动作。
```

---

## 2. Action 和 Telemetry 的区别

Telemetry 的方向是：

```text
PX4 → Python
```

作用是读取状态，例如：

```text
高度
位置
姿态
飞行模式
是否解锁
```

Action 的方向是：

```text
Python → PX4
```

作用是发送命令，例如：

```text
解锁
起飞
降落
返航
```

因此：

```text
Telemetry = 看无人机
Action = 命令无人机
```

---

## 3. 常用 Action 命令

### arm

```python
await drone.action.arm()
```

作用：

```text
解锁无人机，让无人机进入可执行飞行动作的状态。
```

---

### takeoff

```python
await drone.action.takeoff()
```

作用：

```text
让 PX4 执行自动起飞。
```

注意：

```text
takeoff 之前通常需要先 arm。
```

---

### land

```python
await drone.action.land()
```

作用：

```text
让无人机在当前位置自动降落。
```

---

### return_to_launch

```python
await drone.action.return_to_launch()
```

作用：

```text
让无人机返回起飞点并降落。
```

---

### set_takeoff_altitude

```python
await drone.action.set_takeoff_altitude(3.0)
```

作用：

```text
设置自动起飞目标高度。
```

例如：

```text
3.0 表示起飞到约 3 米高度。
```

---

## 4. Action 的控制流程

以起飞为例：

```text
Python 程序
    ↓
MAVSDK Action
    ↓
MAVLink 命令
    ↓
PX4 Commander
    ↓
PX4 控制器
    ↓
电机输出
    ↓
无人机起飞
```

Action 并不是直接控制电机，而是向 PX4 发送高级动作命令。

真正的姿态控制、高度控制、角速度控制和电机分配仍然由 PX4 内部完成。

---

## 5. Action 和 PX4 控制器的关系

调用：

```python
await drone.action.takeoff()
```

并不等于 Python 直接控制高度 PID。

它更像是告诉 PX4：

```text
请进入起飞流程。
```

然后 PX4 内部会完成：

```text
高度控制
姿态控制
角速度控制
控制分配
电机输出
```

所以 Action 是高层接口，不是底层控制器。

---

## 6. 为什么 Action 要配合 Telemetry

Action 负责发命令，但发完命令后，还需要观察无人机是否真的执行成功。

例如起飞后，需要通过 Telemetry 观察：

```text
armed 是否为 True
flight_mode 是否变化
relative_altitude_m 是否上升
roll / pitch 是否稳定
```

因此后续程序应该采用：

```text
Action 发命令
Telemetry 看结果
CSV 记录过程
曲线分析效果
```

---

## 7. 起飞降落的基本流程

后续实际程序可以按这个流程写：

```text
1. 连接 PX4 SITL
2. 等待连接成功
3. 检查 telemetry 状态
4. 设置起飞高度
5. arm 解锁
6. takeoff 起飞
7. 读取高度并等待达到目标高度
8. 悬停几秒
9. land 降落
10. 读取 telemetry 直到降落完成
```

---

## 8. 安全理解

在 PX4 SITL 中，Action 命令只控制仿真无人机。

但在真实无人机上，Action 命令可能会让电机转动，因此必须非常谨慎。

真实无人机执行 Action 前，需要确认：

```text
环境安全
螺旋桨区域无人
电池正常
GPS / EKF 状态正常
飞行模式正确
遥控器和急停措施可用
```

---

## 9. 今日总结

今天理解了 MAVSDK Action 的基本作用。

最重要的结论：

```text
Action 用来发送高级动作命令，Telemetry 用来观察命令执行后的状态变化。
```

一句话总结：

```text
MAVSDK Action 是从“读取 PX4 状态”走向“用 Python 控制 PX4”的第一步。
```
