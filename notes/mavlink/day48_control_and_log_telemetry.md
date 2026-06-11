# Day 48 边控制边记录 Telemetry

## 今日目标

今天使用 MAVSDK Python 实现边控制无人机，边记录 telemetry 数据到 CSV。

本次任务是在 Day 47 的基础上升级：

```text
Day 47：起飞 → 悬停 → 降落
Day 48：起飞 → 悬停 → 降落，同时记录 telemetry
```

---

## 1. 今日完成内容

今天完成完整流程：

```text
连接 PX4 SITL
    ↓
持续读取 telemetry
    ↓
启动 CSV logger
    ↓
arm 解锁
    ↓
takeoff 起飞
    ↓
hover 悬停
    ↓
land 降落
    ↓
保存完整飞行数据
```

---

## 2. 程序路径

程序路径：

```text
code/03_mavsdk_telemetry/action_takeoff_hover_land_log.py
```

运行方法：

```bash
cd ~/uav-learning/code/03_mavsdk_telemetry
source venv/bin/activate
python action_takeoff_hover_land_log.py
```

输出 CSV：

```text
code/03_mavsdk_telemetry/data/takeoff_hover_land_telemetry.csv
```

---

## 3. 本次保存的数据

CSV 中保存：

```text
time_s
mission_phase
armed
flight_mode
latitude_deg
longitude_deg
absolute_altitude_m
relative_altitude_m
roll_deg
pitch_deg
yaw_deg
```

其中最重要的是：

```text
time_s：当前时间
mission_phase：任务阶段
relative_altitude_m：相对高度
roll_deg / pitch_deg / yaw_deg：姿态角
flight_mode：飞行模式
armed：是否解锁
```

---

## 4. 为什么需要 mission_phase

`mission_phase` 用来标记当前任务阶段：

```text
init
arming
takeoff
hover
landing
finished
```

它的意义是：

```text
后续画图时，可以知道某一段高度变化对应起飞、悬停还是降落。
```

例如：

```text
takeoff 阶段：高度上升
hover 阶段：高度保持
landing 阶段：高度下降
```

---

## 5. 程序结构理解

本程序同时运行三类任务：

```text
1. 控制任务
   arm → takeoff → hover → land

2. telemetry 观察任务
   持续读取 position、attitude、flight_mode、armed

3. CSV 记录任务
   每 0.2 秒写入一行最新 telemetry
```

这就是“边控制边记录”。

---

## 6. 今日核心理解

今天理解了：

```text
Action 用来控制无人机；
Telemetry 用来观察无人机；
CSV logger 用来记录无人机全过程状态。
```

完整逻辑是：

```text
Action 发命令
Telemetry 看状态
CSV 保存数据
后续用曲线分析结果
```

---

## 7. 本次实验结果记录

是否连接成功：

```text
是 / 否：
```

是否 arm 成功：

```text
是 / 否：
```

是否 takeoff 成功：

```text
是 / 否：
```

是否 hover 成功：

```text
是 / 否：
```

是否 land 成功：

```text
是 / 否：
```

CSV 是否生成：

```text
是 / 否：
```

CSV 文件行数：

```text
____ 行
```

最大相对高度：

```text
____ m
```

---

## 8. 今日总结

今天完成了 MAVSDK Action 控制和 Telemetry 记录的结合。

最重要的结论：

```text
飞控实验不能只控制，还要记录数据；没有记录，就无法分析飞行过程。
```

一句话总结：

```text
Day 48 的核心是让 Python 程序一边控制 PX4 SITL 飞行，一边把全过程 telemetry 保存下来。
```

