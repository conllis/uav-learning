# Day 09 连接 QGroundControl

## 今日目标

在 Windows 安装 QGroundControl，并连接 WSL Ubuntu 中运行的 PX4 SITL + Gazebo x500 仿真。

---

## 1. 启动 PX4 SITL + Gazebo

```bash
cd ~/PX4-Autopilot
make px4_sitl gz_x500

成功标志：

INFO  [init] Gazebo world is ready
INFO  [init] Spawning Gazebo model
INFO  [gz_bridge] world: default, model: x500_0
pxh>
2. 启动 QGroundControl

QGroundControl 安装在 Windows 端。

打开后正常情况下会自动通过 UDP 连接 PX4 SITL。

3. MAVLink 连接

PX4 和 QGroundControl 之间通过 MAVLink 通信。

常见 UDP 端口：

14550

PX4 终端中可以查看：

mavlink status
4. 连接成功标志
QGroundControl 显示车辆已连接
出现姿态仪
能看到无人机位置
能看到飞行模式
能看到高度、GPS、电池等状态
PX4 中 No connection to the GCS 警告消失或减少
5. 如果没有自动连接

在 QGroundControl 中手动添加 UDP 连接：

Q 图标
→ Application Settings
→ Comm Links
→ Add
→ Type: UDP
→ Listening Port: 14550
→ Connect
6. 今日观察

记录内容：

是否自动连接：
是否看到姿态仪：
是否看到地图位置：
是否看到飞行模式：
是否仍有 Preflight Fail：
是否尝试 Arm / Takeoff / Land：
7. 退出流程

在 PX4 shell 输入：

shutdown

或者关闭 Gazebo 后清理进程：

pkill -f px4
pkill -f gz
今日总结

今天完成 QGroundControl 与 PX4 SITL 的连接测试。QGroundControl 是地面站，PX4 是飞控程序，Gazebo 是仿真环境，三者通过 MAVLink 和仿真接口协同工# Day 09 连接 QGroundControl

