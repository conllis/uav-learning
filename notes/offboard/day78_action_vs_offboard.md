# Day 78 Action 控制 vs Offboard 控制对比

## 1. 今日目标

理解 MAVSDK Action 控制和 Offboard 控制的区别，并明确后续实验中两者的分工。

---

## 2. Action 控制是什么？

Action 控制是 MAVSDK 提供的高级动作接口。

常见命令包括：

- arm
- takeoff
- land
- return_to_launch
- goto_location

Action 的特点是命令层级较高。

例如：

```python
await drone.action.takeoff()
await drone.action.land()

这些命令不需要持续发送 setpoint，而是告诉 PX4 执行一个高级动作。

3. Offboard 控制是什么？

Offboard 控制是外部程序持续向 PX4 发送 setpoint。

常见 setpoint 包括：

位置 setpoint
速度 setpoint
姿态 setpoint

Offboard 的特点是必须持续发送控制目标。

例如：

await drone.offboard.set_position_ned(PositionNedYaw(3.0, 0.0, -3.0, 0.0))

如果 setpoint 中断，PX4 可能退出 Offboard 或触发 failsafe。

4. 两者区别
对比项	Action	Offboard
控制层级	高级命令	连续 setpoint
是否需要持续发送	不需要	需要
适合任务	起飞、降落、返航	悬停、移动、轨迹跟踪
风险	较低	较高
对程序实时性要求	较低	较高
本周用途	起飞和降落	中间轨迹控制
5. 本周采用的原则

后续实验采用：

Action 起飞
    ↓
Offboard 接管
    ↓
持续发送位置 setpoint
    ↓
Action 降落

原因：

Action 起飞更稳定
Offboard 更适合轨迹控制
Action 降落更安全
整个流程更容易记录和分析
6. 今日结论

Action 适合执行高级动作，Offboard 适合执行持续控制。

在当前 PX4 SITL 实验中，最稳妥的流程是：

Action 负责起飞和降落
Offboard 负责悬停、移动到点和方形轨迹

---

# 7. 推荐运行顺序

今天不要一次全跑。按这个顺序：

```text
1. 先跑 offboard_hover_stable.py
2. 确认能起飞、进入 Offboard、悬停、降落
3. 再跑 offboard_move_point_stable.py
4. 最后跑 offboard_square.py
5. 用 plot_offboard.py 画图
6. 写 day78_action_vs_offboard.md

每次运行前，最好重新启动 PX4 SITL：

cd ~/PX4-Autopilot
make px4_sitl gz_x500
8. 今日完成标准

今天完成后，你应该有这些文件：

code/05_offboard_control/offboard_utils.py
code/05_offboard_control/offboard_hover_stable.py
code/05_offboard_control/offboard_move_point_stable.py
code/05_offboard_control/offboard_square.py

data/month3/offboard_hover.csv
data/month3/offboard_move_point.csv
data/month3/offboard_square.csv

scripts/plot_offboard.py

plots/month3/offboard_altitude.png
plots/month3/offboard_attitude.png
plots/month3/offboard_phase.png
plots/month3/offboard_xy_trajectory.png

notes/offboard/day78_action_vs_offboard.md
