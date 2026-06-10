# Day 42 保存 Telemetry 到 CSV

## 今日目标

今天使用 MAVSDK Python 读取 PX4 SITL 的基础 telemetry，并保存到 CSV 文件中，为后续绘制飞行曲线和分析飞行状态做准备。

---

## 1. 为什么要保存 CSV

Day 41 已经可以在终端打印 telemetry 数据，但终端输出不方便后续分析。

保存为 CSV 后，可以用于：

```text
画高度曲线
画 roll / pitch / yaw 姿态曲线
分析飞行模式变化
记录起飞、悬停、降落过程
后续做 Offboard 控制反馈分析
```

---

## 2. 本次保存的数据

本次保存以下字段：

```text
time_s
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

含义：

```text
time_s：程序运行时间
armed：是否解锁
flight_mode：当前飞行模式
latitude_deg：纬度
longitude_deg：经度
absolute_altitude_m：绝对高度
relative_altitude_m：相对起飞点高度
roll_deg：横滚角
pitch_deg：俯仰角
yaw_deg：偏航角
```

---

## 3. 程序路径

程序路径：

```text
code/03_mavsdk_telemetry/log_telemetry_csv.py
```

输出文件：

```text
code/03_mavsdk_telemetry/data/px4_telemetry.csv
```

---

## 4. 运行方法

先启动 PX4 SITL：

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

再打开另一个终端：

```bash
cd ~/uav-learning/code/03_mavsdk_telemetry
source venv/bin/activate
python log_telemetry_csv.py
```

---

## 5. 程序逻辑

程序主要流程：

```text
1. 创建 MAVSDK System 对象
2. 连接 PX4 SITL：udp://:14540
3. 等待 Drone connected
4. 并行读取 position、attitude、flight_mode、armed
5. 把最新 telemetry 保存到 latest 字典
6. 每 0.2 秒写入一行 CSV
7. 记录 30 秒后结束
```

---

## 6. CSV 检查方法

查看是否生成文件：

```bash
ls data
```

查看前几行：

```bash
head data/px4_telemetry.csv
```

查看行数：

```bash
wc -l data/px4_telemetry.csv
```

如果记录 30 秒、间隔 0.2 秒，理论上大约会有 150 行数据，加上表头大约 151 行。

---

## 7. 今日理解

今天理解了：

```text
Telemetry 不只是可以打印到终端，还可以保存为实验数据。
CSV 是后续画图、分析日志、比较控制效果的重要中间文件。
```

MAVSDK 读取 telemetry 的结果，可以用于：

```text
状态监控
飞行记录
控制效果分析
Offboard 控制反馈
```

---

## 8. 今日总结

今天完成了 PX4 telemetry 的 CSV 保存。

最重要的结论：

```text
从今天开始，PX4 SITL 的飞行状态不再只是“看一眼”，而是可以被记录、画图和分析。
```

下一步：

```text
Day 43：读取 CSV 并绘制高度曲线、姿态曲线。
```
