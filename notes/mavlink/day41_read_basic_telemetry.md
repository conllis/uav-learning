# Day 41 读取基础 Telemetry

## 今日目标

今天使用 MAVSDK Python 读取 PX4 SITL 的基础 telemetry 数据，包括位置、高度、姿态、飞行模式和是否解锁。

---

## 1. Telemetry 是什么

Telemetry 是无人机发出来的遥测状态数据。

可以理解为无人机不断汇报：

```text
我现在在哪里？
我现在多高？
我现在姿态是多少？
我现在是什么飞行模式？
我现在有没有解锁？
```

---

## 2. 本次读取的数据

本次读取以下 telemetry：

```text
position
attitude_euler
flight_mode
armed
```

对应含义：

```text
position：经纬度、绝对高度、相对高度
attitude_euler：roll、pitch、yaw
flight_mode：当前飞行模式
armed：是否解锁
```

---

## 3. MAVSDK 连接地址

Day 39 中，PX4 的 MAVLink 状态显示：

```text
instance #1:
mode: Onboard
UDP local port: 14580
remote port: 14540
```

因此本次程序使用：

```text
udp://:14540
```

作为 MAVSDK 连接地址。

---

## 4. 程序路径

本次程序路径：

```text
code/03_mavsdk_telemetry/read_basic_telemetry.py
```

运行方法：

```bash
cd ~/uav-learning/code/03_mavsdk_telemetry
source venv/bin/activate
python read_basic_telemetry.py
```

---

## 5. 程序逻辑

程序主要步骤：

```text
1. 创建 System 对象
2. 连接 PX4 SITL
3. 等待 connection_state 显示已连接
4. 并行读取 position、attitude_euler、flight_mode、armed
5. 每秒打印一次最新 telemetry
6. 运行 30 秒后结束
```

---

## 6. 代码中的异步读取

MAVSDK Python 使用异步方式读取 telemetry。

示例：

```python
async for position in drone.telemetry.position():
    latest["latitude_deg"] = position.latitude_deg
    latest["longitude_deg"] = position.longitude_deg
    latest["relative_altitude_m"] = position.relative_altitude_m
```

含义：

```text
只要 PX4 持续发送位置数据，程序就持续接收并更新最新值。
```

---

## 7. 为什么使用多个 task

position、attitude、flight_mode 和 armed 是不同的数据流。

如果只读取一个数据流，程序可能一直停留在这个循环中。

因此使用：

```python
asyncio.create_task(...)
```

让多个 telemetry 读取任务同时运行。

---

## 8. 今日观察结果

本次是否连接成功：

```text
是 / 否：
```

是否看到 Drone connected：

```text
是 / 否：
```

是否读取到位置：

```text
是 / 否：
```

是否读取到高度：

```text
是 / 否：
```

是否读取到姿态 roll / pitch / yaw：

```text
是 / 否：
```

是否读取到 flight_mode：

```text
是 / 否：
```

是否读取到 armed：

```text
是 / 否：
```

---

## 9. 今日总结

今天完成了 MAVSDK Python 的基础 telemetry 读取。

最重要的理解：

```text
MAVSDK 不只能连接 PX4，还能持续读取 PX4 发出的状态数据。
```

这些 telemetry 数据后续可以用于：

```text
保存 CSV
绘制飞行曲线
分析高度和姿态变化
做 Offboard 控制反馈
```

一句话总结：

```text
Day 41 的核心是从“连接 PX4”升级到“用程序读取 PX4 的飞行状态”。
```
