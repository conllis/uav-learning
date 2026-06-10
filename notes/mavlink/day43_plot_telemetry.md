# Day 43 画 Telemetry 曲线

## 今日目标

今天读取 Day 42 保存的 PX4 telemetry CSV 文件，并绘制高度、姿态和飞行模式曲线，为后续分析飞行状态做准备。

---

## 1. 输入数据

本次使用的 CSV 文件：

```text
code/03_mavsdk_telemetry/data/px4_telemetry.csv
```

该文件由 Day 42 的程序生成：

```text
code/03_mavsdk_telemetry/log_telemetry_csv.py
```

CSV 中主要字段包括：

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

---

## 2. 画图脚本

本次创建画图脚本：

```text
code/03_mavsdk_telemetry/scripts/plot_telemetry.py
```

脚本主要完成：

```text
1. 读取 data/px4_telemetry.csv
2. 绘制相对高度曲线
3. 绘制 roll / pitch / yaw 姿态曲线
4. 绘制飞行模式变化曲线
5. 输出基础统计信息
```

---

## 3. 输出图片

本次生成图片：

```text
code/03_mavsdk_telemetry/plots/relative_altitude.png
code/03_mavsdk_telemetry/plots/attitude_euler.png
code/03_mavsdk_telemetry/plots/flight_mode.png
```

---

## 4. 高度曲线理解

`relative_altitude.png` 表示相对起飞点高度随时间变化。

如果无人机没有起飞：

```text
relative_altitude_m 通常接近 0
曲线基本平直
```

如果后续无人机起飞：

```text
高度曲线应该先上升，然后逐渐稳定
```

高度曲线后续可以用来分析：

```text
起飞过程
悬停稳定性
降落过程
高度控制效果
```

---

## 5. 姿态曲线理解

`attitude_euler.png` 表示 roll、pitch、yaw 随时间变化。

含义：

```text
roll：横滚角，表示左右倾斜
pitch：俯仰角，表示前后俯仰
yaw：偏航角，表示机头方向
```

如果无人机静止在地面：

```text
roll / pitch 通常接近 0
yaw 通常保持某个固定方向
```

如果后续无人机移动：

```text
向前飞时 pitch 可能变化
左右移动时 roll 可能变化
转向时 yaw 可能变化
```

---

## 6. 飞行模式曲线理解

`flight_mode.png` 用数字编号表示飞行模式变化。

它可以帮助观察：

```text
飞行模式是否发生切换
比如 HOLD、TAKEOFF、LAND、OFFBOARD 等
```

如果没有执行控制命令，飞行模式可能基本保持不变。

---

## 7. 今日理解

今天理解了：

```text
Telemetry CSV 可以进一步转换成曲线；
曲线比终端输出更适合观察飞行状态变化；
高度曲线可以用于分析高度控制；
姿态曲线可以用于分析 roll / pitch / yaw 的变化；
飞行模式曲线可以用于观察任务阶段变化。
```

---

## 8. 今日总结

今天完成了从“保存 telemetry 数据”到“画 telemetry 曲线”的过程。

最重要的结论：

```text
CSV 是飞行数据记录，曲线是飞行状态分析入口。
```

一句话总结：

```text
Day 43 的核心是把 PX4 telemetry 从数据表变成可观察、可分析的飞行曲线。
```
