# Day 10 完成 PX4 SITL 仿真起飞和降落

## 今日目标

在 PX4 SITL + Gazebo x500 仿真环境中，完成一次起飞、悬停和降落流程。

---

## 1. 启动仿真

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500

成功标志：

INFO  [init] Gazebo world is ready
INFO  [init] Spawning Gazebo model
INFO  [gz_bridge] world: default, model: x500_0
pxh>
2. 检查状态
commander status
sensors status
listener vehicle_local_position 1
3. 解锁
commander arm
4. 起飞
commander takeoff

观察 Gazebo 中 x500 是否离地上升。

5. 查看位置
listener vehicle_local_position 1

注意：PX4 本地坐标常用 NED 坐标系，向上飞时 z 可能是负值。

6. 降落
commander land
7. 上锁和退出
commander disarm
shutdown
8. 今日观察记录
是否成功 Arm：
是否成功 Takeoff：
是否成功悬停：
是否成功 Land：
是否出现 Preflight Fail：
Gazebo 中飞机是否正常：
9. 今日总结

今天完成了 PX4 SITL + Gazebo x500 的基础飞行流程，理解了 Arm、Takeoff、Land、Disarm 的基本作用。

commander arm：解锁无人机
commander takeoff：执行起飞
commander land：执行降落
commander disarm：上锁
shutdown：退出 PX4 SITL
