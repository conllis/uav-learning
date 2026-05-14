cd ~/uav-learning
mkdir -p notes/qgroundcontrol
nano notes/qgroundcontrol/day12_simple_mission.md# Day 12 执行简单航点任务

## 今日目标

使用 QGroundControl 给 PX4 SITL + Gazebo x500 上传一个简单航点任务，并观察无人机自动执行任务。

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
2. 打开 QGroundControl

QGroundControl 连接成功后应看到：

姿态仪
地图位置
飞行模式
高度
GPS / 定位状态
3. 创建简单航点任务

在 QGroundControl 中：

Plan
→ 添加 Takeoff
→ 添加 3 到 4 个 Waypoint
→ 设置高度 10 m
→ 添加 Land 或 Return
→ Upload
4. 执行任务
Fly
→ Arm
→ Start Mission

观察 Gazebo 中无人机是否：

起飞
飞向航点 1
飞向航点 2
飞向航点 3
降落或返航
5. PX4 shell 观察命令
commander status
listener vehicle_status 1
listener vehicle_local_position 1
listener vehicle_global_position 1
6. 常见问题
Mission rejected: empty

说明 PX4 没有收到任务，通常是没有点击 Upload。

No connection to the GCS

说明 QGroundControl 没有连接成功。

Arm failed

可能是 EKF、定位、GCS 或安全检查未通过。

7. 今日实验记录
QGroundControl 是否连接成功：
是否成功上传任务：
航点数量：
任务高度：
是否成功 Arm：
是否成功 Start Mission：
是否完成全部航点：
是否成功 Land / Return：
出现的问题：
解决方法：
今日总结

今天学习了 PX4 Mission 模式的基本流程。

QGroundControl 用于规划和上传航点任务，PX4 接收任务后进入 Mission 模式，Gazebo 中的 x500 无人机会按照航点自动飞行。
