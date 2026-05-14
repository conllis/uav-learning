# Day 13 PX4 仿真截图与日志索引

## 一、实验目标

保存 PX4 SITL + Gazebo x500 仿真实验的截图和日志。

---

## 二、实验命令

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500
三、成功标志
INFO  [init] Gazebo world is ready
INFO  [init] Spawning Gazebo model
INFO  [gz_bridge] world: default, model: x500_0
pxh>
四、截图文件
screenshots/day13/gazebo_x500_spawned.png
screenshots/day13/px4_terminal_pxh.png
screenshots/day13/gazebo_takeoff.png
screenshots/day13/gazebo_landing.png

实际保存的文件以目录中为准。

五、PX4 飞行日志

PX4 原始日志目录：

~/PX4-Autopilot/build/px4_sitl_default/log/

本次复制到：

~/uav-learning/logs/day13/

.ulg 文件用于后续飞行数据分析，可以使用 Flight Review 或 pyulog 解析。

六、今日记录
是否成功启动 Gazebo：
是否看到 x500 模型：
是否进入 pxh>：
是否完成起飞：
是否完成降落：
是否保存 .ulg 日志：
是否保存截图：
遇到的问题：
解决方法：
七、今日总结

今天完成了 PX4 SITL + Gazebo x500 仿真实验的证据保存，包括 Gazebo 截图、PX4 终端截图、PX4 .ulg 飞行日志和实验索引文档。

这一步的意义是：以后不仅能说“我跑通过 PX4 仿真”，还可以用截图和日志证明实验过程。
