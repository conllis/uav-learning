# 第 2 个月第 2 周总结：MAVSDK Telemetry 入门

## 一、本周学习目标

本周的主要目标是从“理解 MAVLink / MAVSDK 概念”进入“用 Python 程序连接 PX4 SITL 并读取 telemetry 数据”。

本周重点不是控制无人机，而是建立外部程序和 PX4 之间的通信能力。

本周主线：

```text
理解 MAVLink / MAVSDK
    ↓
启动 PX4 SITL 并确认 MAVLink 端口
    ↓
安装 MAVSDK Python
    ↓
用 Python 连接 PX4
    ↓
读取基础 telemetry
    ↓
保存 telemetry 到 CSV
    ↓
绘制 telemetry 曲线
```

---

## 二、本周完成内容

### 1. 理解 MAVLink / MAVSDK

本周首先学习了 MAVLink 和 MAVSDK 的基本概念。

核心理解：

```text
MAVLink 是无人机通信协议；
MAVSDK 是基于 MAVLink 的开发工具；
QGroundControl 是人使用的地面站；
MAVSDK 是程序使用的控制库。
```

MAVLink 负责规定无人机和外部系统之间如何传消息。

MAVSDK 则把底层 MAVLink 消息封装成更容易使用的 Python / C++ API。

---

### 2. 启动 PX4 SITL 并确认 MAVLink 端口

本周启动了 PX4 SITL：

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

并使用：

```bash
mavlink status
```

查看 MAVLink 状态。

观察到关键实例：

```text
instance #1:
mode: Onboard
UDP local port: 14580
remote port: 14540
```

因此后续 MAVSDK Python 程序优先使用：

```text
udp://:14540
```

作为连接地址。

同时也观察到 QGroundControl 对应的 GCS 通信端口，说明 PX4 SITL 已经可以通过 MAVLink 和外部程序通信。

---

### 3. 安装并测试 MAVSDK Python

本周创建了 MAVSDK 项目目录：

```text
code/03_mavsdk_telemetry
```

创建 Python 虚拟环境：

```bash
python3 -m venv venv
source venv/bin/activate
```

安装 MAVSDK Python：

```bash
pip install mavsdk
```

并编写最小连接测试程序：

```text
code/03_mavsdk_telemetry/connect_test.py
```

测试目标：

```text
确认 Python 程序能通过 MAVSDK 连接 PX4 SITL
```

成功标志：

```text
Drone connected!
```

---

### 4. 读取基础 telemetry

本周编写了基础 telemetry 读取程序：

```text
code/03_mavsdk_telemetry/read_basic_telemetry.py
```

读取的数据包括：

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
flight_mode：飞行模式
armed：是否解锁
```

通过该程序，我第一次用自己的 Python 程序读取到了 PX4 SITL 的飞行状态。

---

### 5. 保存 telemetry 到 CSV

本周编写了 CSV 记录程序：

```text
code/03_mavsdk_telemetry/log_telemetry_csv.py
```

输出文件：

```text
code/03_mavsdk_telemetry/data/px4_telemetry.csv
```

CSV 中保存：

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

这一步的意义是：

```text
把 PX4 的实时状态变成可保存、可复现、可分析的数据文件。
```

---

### 6. 绘制 telemetry 曲线

本周编写画图脚本：

```text
code/03_mavsdk_telemetry/scripts/plot_telemetry.py
```

生成图片：

```text
code/03_mavsdk_telemetry/plots/relative_altitude.png
code/03_mavsdk_telemetry/plots/attitude_euler.png
code/03_mavsdk_telemetry/plots/flight_mode.png
```

通过画图，能够更直观地观察：

```text
高度是否变化
roll / pitch / yaw 是否稳定
飞行模式是否切换
```

---

## 三、本周项目文件

本周主要项目目录：

```text
code/03_mavsdk_telemetry/
```

主要文件：

```text
connect_test.py
read_basic_telemetry.py
log_telemetry_csv.py
scripts/plot_telemetry.py
data/px4_telemetry.csv
plots/relative_altitude.png
plots/attitude_euler.png
plots/flight_mode.png
```

本周笔记：

```text
notes/mavlink/day38_mavlink_mavsdk_basic.md
notes/mavlink/day39_px4_mavlink_port.md
notes/mavlink/day40_mavsdk_python_install_test.md
notes/mavlink/day41_read_basic_telemetry.md
notes/mavlink/day42_log_telemetry_csv.md
notes/mavlink/day43_plot_telemetry.md
```

---

## 四、本周最重要的理解

### 1. MAVLink 和 MAVSDK 的关系

```text
MAVLink 是通信协议；
MAVSDK 是开发工具。
```

可以类比为：

```text
MAVLink 是无人机通信语言；
MAVSDK 是帮程序员说这门语言的工具。
```

---

### 2. QGroundControl 和 MAVSDK 的区别

```text
QGroundControl：给人使用，通过界面查看和控制无人机；
MAVSDK：给程序使用，通过代码读取和控制无人机。
```

它们底层都通过 MAVLink 与 PX4 通信。

---

### 3. Telemetry 的意义

Telemetry 是无人机持续发出的状态数据。

包括：

```text
位置
高度
速度
姿态
飞行模式
电池
是否解锁
```

后续做起飞、悬停、降落和 Offboard 控制时，telemetry 是外部程序判断无人机状态的基础。

---

### 4. CSV 的意义

终端输出只能临时查看。

CSV 可以用于：

```text
保存实验数据
复现飞行过程
画曲线
分析控制效果
写实验报告
```

因此，从 Day 42 开始，telemetry 不只是“看见”，而是可以被记录和分析。

---

### 5. 曲线的意义

曲线能直观看出飞行状态变化。

例如：

```text
高度曲线：观察起飞、悬停、降落
姿态曲线：观察 roll / pitch / yaw 变化
飞行模式曲线：观察模式切换
```

这为后续分析 MAVSDK Action 起飞、悬停、降落过程打基础。

---

## 五、本周存在的问题

目前还存在以下问题：

```text
1. 目前只读取状态，还没有控制无人机；
2. 当前 telemetry 数据多数来自静止状态，曲线变化不明显；
3. 还没有记录速度、电池、GPS 健康状态等更多 telemetry；
4. 还没有实现自动起飞、悬停和降落；
5. 还没有结合 telemetry 判断任务是否完成；
6. 对 MAVLink 底层消息格式仍然只是初步理解。
```

---

## 六、下周计划

下周重点从“读取 PX4 状态”进入“用 MAVSDK 控制 PX4”。

计划内容：

```text
Day 44：理解 MAVSDK Action
Day 45：用 MAVSDK 解锁和起飞
Day 46：起飞后悬停并读取 telemetry
Day 47：自动降落
Day 48：记录起飞、悬停、降落全过程 CSV
Day 49：画起飞降落过程曲线
Day 50：第 3 周总结
```

下周目标：

```text
用 Python 程序完成 PX4 SITL 的自动起飞、悬停和降落，并记录 telemetry 数据。
```

---

## 七、本周总结

本周完成了 MAVSDK Telemetry 入门。

最重要的收获是：

```text
已经可以用自己的 Python 程序连接 PX4 SITL，并读取、保存、绘制基础 telemetry 数据。
```

一句话总结：

```text
本周完成了从“理解 MAVLink / MAVSDK”到“用 Python 读取 PX4 飞行状态”的过渡，为后续 MAVSDK Action 控制无人机打下基础。
```
