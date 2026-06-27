# 第 3 个月第 3 周总结：Offboard 强化与轨迹记录

## 1. 本周目标

本周目标是进入 Offboard 控制阶段，完成 PX4 SITL 中的外部位置控制实验。

原计划包括：

1. 整理 Offboard 问题记录与稳定流程。
2. 完成 Offboard 悬停稳定版。
3. 完成 Offboard 移动到一个点。
4. 完成 Offboard 方形轨迹。
5. 保存 telemetry CSV。
6. 绘制高度、姿态、任务阶段曲线。
7. 对比 Action 控制和 Offboard 控制的区别。

本周核心流程确定为：

```text
Action 起飞
    ↓
Offboard 接管
    ↓
持续发送位置 setpoint
    ↓
记录 telemetry
    ↓
Action 降落
```

---

## 2. 本周完成内容

### 2.1 Day 73：Offboard 问题记录与稳定流程

完成文件：

```text
notes/offboard/day73_offboard_debug_review.md
```

主要结论：

Offboard 不适合直接从地面“盲目起飞”，后续统一采用：

```text
Action 起飞 + Offboard 接管 + Action 降落
```

原因：

* Action 起飞更稳定。
* Offboard 更适合中间阶段的持续 setpoint 控制。
* Action 降落更安全。
* 这种流程更容易记录 telemetry 和分析问题。

---

### 2.2 Day 74：Offboard 悬停稳定版

完成代码：

```text
code/05_offboard_control/offboard_utils.py
code/05_offboard_control/offboard_hover_stable.py
```

初步运行结果：

* MAVSDK 能连接 PX4 SITL。
* PX4 health 检查通过。
* Action takeoff 命令可以发送。
* Gazebo 中无人机能够起飞。
* Ctrl+C 后 safe_land 能执行。
* CSV 能保存到：

```text
data/month3/offboard_hover.csv
```

遇到的问题：

1. 出现过端口占用：

```text
bind error: Address in use
```

初步判断是之前的 MAVSDK 进程、telemetry bridge、action command node 或 offboard 脚本没有完全关闭。

处理方法：

```bash
pkill -f mavsdk_server
pkill -f px4_telemetry_bridge
pkill -f px4_action_command_node
pkill -f offboard_hover_stable.py
```

2. Gazebo 中无人机已经起飞，但终端打印的 `relative_altitude_m` 一直为 0。

初步判断：

`position.relative_altitude_m` 在当前 PX4 SITL / Gazebo 环境下没有正确反映实际离地高度。

后续改用：

```python
local_altitude_m = -position_velocity_ned.position.down_m
```

因为 Offboard 使用的是 NED 本地坐标系，向上 3 米对应：

```text
down_m = -3
```

---

### 2.3 Day 75：Offboard 移动到一个点

计划目标：

```text
起飞到 3 m
进入 Offboard
悬停
移动到 north=3, east=0, down=-3
保持 10 秒
降落
记录 CSV
```

当前状态：

```text
代码已规划，仍需要在修正高度判断和 Gazebo GUI 恢复后重新测试。
```

待生成文件：

```text
code/05_offboard_control/offboard_move_point_stable.py
data/month3/offboard_move_point.csv
plots/month3/offboard_move_point_altitude.png
```

---

### 2.4 Day 76：Offboard 方形轨迹

计划轨迹：

```text
P0: north=0, east=0, down=-3
P1: north=3, east=0, down=-3
P2: north=3, east=3, down=-3
P3: north=0, east=3, down=-3
P4: north=0, east=0, down=-3
```

当前状态：

```text
代码已规划，仍需要在悬停和移动到点稳定后测试。
```

待生成文件：

```text
code/05_offboard_control/offboard_square.py
data/month3/offboard_square.csv
```

---

### 2.5 Day 77：绘制 Offboard 曲线

计划绘制：

```text
plots/month3/offboard_altitude.png
plots/month3/offboard_attitude.png
plots/month3/offboard_phase.png
plots/month3/offboard_xy_trajectory.png
```

当前注意点：

由于 `relative_altitude_m` 可能一直为 0，后续高度曲线不应只使用 `relative_altitude_m`，而应优先使用：

```python
local_altitude_m = -down_m
```

也就是说，后续画图时应从 CSV 的 `down_m` 字段计算本地高度。

---

### 2.6 Day 78：Action 控制 vs Offboard 控制对比

完成笔记：

```text
notes/offboard/day78_action_vs_offboard.md
```

核心理解：

Action 控制适合高级动作：

* arm
* takeoff
* land
* return_to_launch

Offboard 控制适合持续 setpoint 控制：

* 悬停
* 移动到点
* 方形轨迹
* 轨迹跟踪

本周采用的原则是：

```text
Action 负责起飞和降落；
Offboard 负责中间的持续轨迹控制。
```

---

## 3. Offboard 是否成功进入？

当前结论：

```text
暂未完全确认稳定进入 Offboard。
```

原因：

虽然 Action 起飞已经在 Gazebo 中有效，但由于高度判断使用了 `relative_altitude_m`，终端一直显示 0 m，导致脚本没有进入后续 Offboard 接管阶段。

后续需要修正：

```python
local_altitude_m = -position_velocity_ned.position.down_m
```

然后重新测试 Offboard start 是否成功。

---

## 4. 悬停是否成功？

当前结论：

```text
悬停流程已经写好，但需要修正高度判断后复测。
```

已完成：

* 连接 PX4。
* health 检查。
* Action 起飞。
* CSV 记录。
* safe_land。
* 异常处理。

待完成：

* 使用 NED 高度判断起飞完成。
* 成功进入 Offboard。
* 保持 `PositionNedYaw(0, 0, -3, 0)`。
* 观察是否能稳定悬停。

---

## 5. 移动到点是否成功？

当前结论：

```text
尚未完成稳定验证。
```

原因：

应先保证悬停实验稳定，再进行移动到点实验。

后续验证目标：

```text
north=3
east=0
down=-3
```

需要记录：

* setpoint 是否切换。
* 本地位置 north/east/down 是否变化。
* 是否能保持目标点附近。
* 是否能正常降落。

---

## 6. 方形轨迹是否完成？

当前结论：

```text
尚未完成稳定验证。
```

原因：

方形轨迹依赖前两个实验：

1. Offboard 悬停稳定。
2. 移动到一个点稳定。

后续应在这两个实验完成后，再测试方形轨迹。

---

## 7. 本周遇到的问题

### 问题 1：MAVSDK 端口占用

现象：

```text
bind error: Address in use
```

原因：

可能有残留进程占用 MAVSDK / UDP 端口。

处理：

```bash
pkill -f mavsdk_server
pkill -f px4_telemetry_bridge
pkill -f px4_action_command_node
pkill -f offboard_hover_stable.py
```

---

### 问题 2：Gazebo 起飞但 relative_altitude_m 为 0

现象：

```text
Gazebo 中无人机已经起飞
终端打印高度仍然是 0.00 m
```

判断：

起飞命令有效，但高度读取字段不合适。

解决：

后续使用 NED 本地坐标：

```python
local_altitude_m = -down_m
```

---

### 问题 3：Gazebo GUI 不加载

现象：

```text
PX4 可能在运行，但 Gazebo 可视化页面没有显示。
```

处理方法：

清理进程：

```bash
pkill -f px4
pkill -f gz
pkill -f gazebo
pkill -f mavsdk_server
```

重新启动：

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
```

如果仍然不显示，需要检查：

```bash
echo $DISPLAY
echo $WAYLAND_DISPLAY
echo $HEADLESS
```

---

## 8. 后续处理计划

下一步不直接跳到更复杂轨迹，而是按顺序复测：

1. 修正 `wait_until_altitude()`，使用 `-down_m` 判断高度。
2. 重新运行 `offboard_hover_stable.py`。
3. 确认能进入 Offboard 并悬停。
4. 再运行 `offboard_move_point_stable.py`。
5. 最后运行 `offboard_square.py`。
6. 用 `plot_offboard.py` 画图。
7. 把曲线和问题记录补充到报告中。

---

## 9. 本周最大收获

本周最大的收获是理解了 Action 和 Offboard 的分工：

```text
Action 是高级动作控制；
Offboard 是持续 setpoint 控制。
```

并且明确了后续稳定流程：

```text
Action 起飞
    ↓
Offboard 接管
    ↓
持续发送 setpoint
    ↓
记录 telemetry
    ↓
Action 降落
```

虽然本周 Offboard 轨迹还没有完全跑通，但已经定位了关键问题：

```text
不能只依赖 relative_altitude_m；
后续应使用 NED 坐标 down_m 进行高度判断。
```

---

## 10. 第 3 周结论

第 3 周完成了 Offboard 稳定流程设计、悬停脚本初步测试、CSV 记录框架和 Action / Offboard 分工总结。

当前阶段结论：

```text
Offboard 项目已经进入实测阶段，但仍需要修正高度判断、清理端口占用、恢复 Gazebo GUI 后继续复测。
```

下周进入传感器融合和 STM32/FreeRTOS 补齐之前，建议先抽时间把 Offboard hover 复测成功，再继续 move point 和 square trajectory。
