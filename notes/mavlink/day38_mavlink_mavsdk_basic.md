# Day 38 MAVLink / MAVSDK 基础理解

## 今日目标

今天学习 MAVLink、MAVSDK、QGroundControl、Telemetry、Action 和 Offboard 的基本概念，为后续用程序读取和控制 PX4 SITL 做准备。

---

## 1. MAVLink 是什么

MAVLink 是无人机通信协议。

它规定了无人机、地面站、伴随计算机和外部程序之间如何传递消息。

MAVLink 可以传递两类信息：

```text
1. 无人机状态数据
2. 外部控制命令
```

无人机状态数据包括：

```text
位置
高度
速度
姿态
角速度
电池
GPS
飞行模式
是否解锁
```

外部控制命令包括：

```text
解锁
起飞
降落
返航
切换模式
发送目标位置
发送速度指令
```

一句话理解：

```text
MAVLink 是无人机系统之间通信使用的消息语言。
```

---

## 2. MAVSDK 是什么

MAVSDK 是一个开发库。

它把底层 MAVLink 消息封装成更容易使用的 API。

使用 MAVSDK 时，程序员不需要手动构造 MAVLink 数据包，而是可以直接调用函数。

例如：

```python
await drone.action.arm()
await drone.action.takeoff()
```

一句话理解：

```text
MAVSDK 是帮助程序员使用 MAVLink 控制无人机的工具包。
```

---

## 3. MAVLink 和 MAVSDK 的区别

```text
MAVLink：底层通信协议
MAVSDK：上层开发库
```

可以类比为：

```text
MAVLink = 无人机通信语言
MAVSDK = 帮你说这门语言的翻译工具
```

---

## 4. QGroundControl 和 MAVSDK 的区别

QGroundControl 是地面站软件，主要给人使用。

MAVSDK 是编程库，主要给程序使用。

对比：

```text
QGroundControl：用鼠标点击，手动控制无人机
MAVSDK：写程序，自动读取和控制无人机
MAVLink：它们底层都使用的通信协议
```

---

## 5. Telemetry 是什么

Telemetry 是遥测数据，也就是无人机发出来的状态信息。

常见 telemetry 包括：

```text
位置
高度
速度
姿态
角速度
电池
GPS 状态
飞行模式
是否解锁
```

可以理解为无人机不断汇报：

```text
我现在在哪里
我现在多高
我现在歪没歪
我现在电量多少
我现在是什么模式
```

后续要用 MAVSDK 读取 PX4 SITL 的 telemetry 数据。

---

## 6. Action 是什么

Action 是 MAVSDK 中用于发送常见高级动作命令的模块。

常见 Action 包括：

```text
arm：解锁
disarm：上锁
takeoff：起飞
land：降落
return_to_launch：返航
```

Action 适合实现简单自动任务：

```text
连接 PX4
解锁
起飞
悬停
降落
```

---

## 7. Offboard 是什么

Offboard 是外部控制模式。

在 Offboard 中，外部程序持续向 PX4 发送 setpoint。

setpoint 可以是：

```text
目标位置
目标速度
目标姿态
目标角速度
```

Offboard 和 Action 的区别：

```text
Action：发送高级动作命令，例如起飞、降落
Offboard：持续发送控制目标，由外部程序更细致地控制无人机
```

Offboard 的关键点：

```text
不能只发送一次 setpoint
必须持续发送 setpoint
```

如果外部程序停止发送 setpoint，PX4 可能会退出 Offboard 或触发安全保护。

---

## 8. 和 PX4 数据流的关系

PX4 内部有状态估计和控制链路。

MAVSDK 可以做两件事：

### 读取 PX4 状态

例如读取：

```text
姿态
位置
高度
飞行模式
是否解锁
```

这些对应 PX4 内部的状态数据。

### 发送控制命令

例如发送：

```text
起飞
降落
目标位置
目标速度
Offboard setpoint
```

这些会影响 PX4 的控制目标和飞行状态。

---

## 9. 本阶段学习目标

接下来几天要完成：

```text
1. 启动 PX4 SITL
2. 确认 MAVLink 端口
3. 安装 MAVSDK Python
4. 用 MAVSDK 连接 PX4
5. 读取 telemetry
6. 保存 telemetry 到 CSV
7. 画高度和姿态曲线
```

---

## 10. 今日总结

今天理解了 MAVLink 和 MAVSDK 的基本关系。

最重要的结论：

```text
MAVLink 是通信协议；
MAVSDK 是基于 MAVLink 的开发工具；
Telemetry 用于读取无人机状态；
Action 用于起飞、降落等高级命令；
Offboard 用于持续发送 setpoint，实现更细致的外部控制。
```

一句话总结：

```text
MAVSDK 是从“看无人机状态”走向“用代码控制无人机”的入口。
```
