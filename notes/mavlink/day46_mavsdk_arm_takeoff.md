# Day 46 实现自动解锁 + 起飞

## 今日目标

今天使用 MAVSDK Python 的 Action 模块，让 PX4 SITL 自动完成解锁和起飞。

---

## 1. 今日完成内容

今天完成：

```text
1. 启动 PX4 SITL
2. 使用 MAVSDK Python 连接 PX4
3. 等待 PX4 connection_state 连接成功
4. 等待 health 状态 ready
5. 设置起飞高度为 3 m
6. 使用 Action arm 解锁
7. 使用 Action takeoff 起飞
8. 使用 Telemetry 观察相对高度
9. 判断是否接近目标起飞高度
```

---

## 2. 程序路径

本次程序路径：

```text
code/03_mavsdk_telemetry/action_arm_takeoff.py
```

运行方法：

```bash
cd ~/uav-learning/code/03_mavsdk_telemetry
source venv/bin/activate
python action_arm_takeoff.py
```

---

## 3. 本次控制流程

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
Gazebo 无人机起飞
```

Action 不是直接控制电机，而是向 PX4 发送高级飞行动作命令。

PX4 内部仍然负责：

```text
高度控制
姿态控制
角速度控制
控制分配
电机输出
```

---

## 4. 本次使用的 Action 命令

### set_takeoff_altitude

```python
await drone.action.set_takeoff_altitude(3.0)
```

含义：

```text
设置自动起飞目标高度为 3 m。
```

---

### arm

```python
await drone.action.arm()
```

含义：

```text
解锁无人机，让无人机进入可飞状态。
```

---

### takeoff

```python
await drone.action.takeoff()
```

含义：

```text
让 PX4 执行自动起飞。
```

---

## 5. 为什么要等待 health ready

程序中等待：

```text
global_position_ok=True
home_position_ok=True
```

原因是 PX4 需要确认定位和 home position 正常，才更容易通过解锁和起飞检查。

如果 PX4 没准备好，可能会拒绝 arm 或 takeoff。

---

## 6. 为什么要用 Telemetry 观察高度

Action 发出 takeoff 命令，并不代表无人机已经到达目标高度。

所以需要读取：

```text
relative_altitude_m
```

观察高度是否从 0 m 上升到接近 3 m。

本次判断逻辑：

```text
如果 relative_altitude_m >= 2.5 m
则认为接近 3 m 起飞高度。
```

---

## 7. 本次实验结果记录

是否连接成功：

```text
是 / 否：
```

是否 health ready：

```text
是 / 否：
```

是否 arm 成功：

```text
是 / 否：
```

是否 takeoff 命令发送成功：

```text
是 / 否：
```

最大相对高度：

```text
____ m
```

是否接近 3 m：

```text
是 / 否：
```

测试后是否手动降落：

```text
是 / 否：
```

---

## 8. 今日理解

今天理解了：

```text
Telemetry 是读取状态；
Action 是发送命令；
Action 命令发出后，必须用 Telemetry 判断无人机是否真的执行成功。
```

本次起飞任务中：

```text
Action 负责 arm 和 takeoff；
Telemetry 负责观察高度变化。
```

---

## 9. 今日总结

今天完成了第一次用 Python 程序控制 PX4 SITL 自动解锁和起飞。

最重要的结论：

```text
MAVSDK Action 是控制 PX4 执行高级飞行动作的入口。
```

一句话总结：

```text
Day 46 的核心是从“读取 PX4 状态”升级到“用 Python 命令 PX4 起飞”。
```
