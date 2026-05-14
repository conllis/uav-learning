# 阶段记录 01：无人机飞控学习环境搭建与 PX4 SITL 初步运行

## 一、阶段时间

第 1 阶段：Day 1 - Day 14

## 二、阶段目标

本阶段目标是完成无人机飞控学习的基础环境搭建，初步跑通 PX4 SITL + Gazebo 仿真流程，并建立个人学习仓库，为后续飞控算法、航点任务、日志分析和 ROS/MAVLink 控制打基础。

---

## 三、当前学习主线

我的研一学习主线是：

```text
Linux / Git / VS Code
↓
C/C++ / CMake / Python
↓
PX4 / Gazebo / QGroundControl
↓
飞控原理 / 仿真飞行 / 日志分析
↓
MAVLink / ROS 2 / Offboard 控制
↓
传感器融合 / EKF / 飞控算法研究
四、已完成内容
1. WSL Ubuntu 环境搭建

已在 Windows 上配置 WSL Ubuntu，并将其作为后续 PX4、C++、Python、Gazebo 开发环境。

常用入口：

wsl

主要开发目录：

~/uav-learning
~/PX4-Autopilot
2. Git 与学习仓库建立

已建立个人学习仓库：

~/uav-learning

仓库结构包括：

uav-learning/
├── notes/
├── reports/
├── code/
├── screenshots/
├── logs/
├── scripts/
└── README.md

目前已经能够完成：

git status
git add .
git commit -m "message"
git push

并解决过远程分支 upstream、rebase 冲突、README 冲突等问题。

3. Linux 基础命令练习

已完成 Linux 基础命令练习，包括：

pwd
ls
cd
mkdir
touch
echo
cat
cp
mv
rm
find
grep
nano

理解了目录、文件、路径、文本查看、查找、搜索等基本操作。

4. C/C++、CMake、Python 环境配置

已完成基础开发工具安装：

sudo apt install -y build-essential gdb cmake make ninja-build pkg-config
sudo apt install -y python3 python3-pip python3-venv

已理解：

gcc / g++：编译器
CMake：构建系统生成工具
make / ninja：构建执行工具
venv：Python 虚拟环境
pip：Python 包管理工具

并完成了 C++ + CMake 测试项目和 Python 虚拟环境测试。

5. PX4、Gazebo、QGroundControl 基本概念理解

已理解三者关系：

QGroundControl：地面站
PX4 SITL：飞控程序
Gazebo：虚拟无人机和仿真世界

三者关系：

QGroundControl
    ↑↓ MAVLink
PX4 SITL
    ↑↓ Gazebo Bridge
Gazebo x500
6. PX4-Autopilot 克隆与依赖安装

已完成 PX4-Autopilot 主仓库克隆：

git clone git@github.com:PX4/PX4-Autopilot.git

处理过的问题包括：

GitHub HTTPS 下载失败
submodule 下载失败
pip 下载 argcomplete / cerberus 超时
Gazebo 依赖缺失
OpenCV 缺失
gz_x500 target 不存在

主要解决方法：

git config --global url."git@github.com:".insteadOf "https://github.com/"
git submodule update --init --recursive --jobs 1
python3 -m pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
sudo apt install -y gz-harmonic
sudo apt install -y libopencv-dev python3-opencv
make distclean
7. PX4 SITL 编译成功

已成功执行：

cd ~/PX4-Autopilot
make px4_sitl

出现过：

ninja: no work to do.

已理解这不是错误，而是表示 PX4 已经编译完成，没有新的内容需要重新编译。

8. PX4 + Gazebo x500 仿真启动成功

已成功执行：

cd ~/PX4-Autopilot
make px4_sitl gz_x500

成功标志：

INFO  [init] Gazebo simulator 8.11.0
INFO  [init] Gazebo world is ready
INFO  [init] Spawning Gazebo model
INFO  [gz_bridge] world: default, model: x500_0
pxh>

说明：

PX4 SITL 已启动
Gazebo Sim 已启动
x500 四旋翼模型已生成
PX4 与 Gazebo 已建立连接
9. 初步了解 PX4 shell

已接触 PX4 shell：

pxh>

常用命令包括：

commander status
sensors status
listener vehicle_status 1
listener vehicle_local_position 1
param show SYS_AUTOSTART
shutdown
10. 初步了解飞行模式

已了解 PX4 常见飞行模式：

Stabilized
Altitude
Position
Hold
Mission
Return
Land
Offboard

当前理解：

Position：PX4 帮助保持位置
Hold：PX4 自动悬停
Mission：执行航点任务
Return：返航
Land：降落
Offboard：外部程序持续发送 setpoint 控制无人机
11. QGroundControl 连接尝试

已尝试连接 Windows 端 QGroundControl。

目前遇到的问题：

Preflight Fail: No connection to the GCS

已初步判断可能与 WSL2 和 Windows 之间的 UDP / MAVLink 通信有关。

已尝试方向：

手动添加 UDP 14550
查看 PX4 MAVLink 端口
尝试 MAV_0_BROADCAST
尝试 mavlink start

该问题仍需后续继续排查。

12. PX4 日志查找与保存

已找到 PX4 SITL 生成的 .ulg 日志，实际路径为：

~/PX4-Autopilot/build/px4_sitl_default/rootfs/log/

示例日志：

/home/zzz/PX4-Autopilot/build/px4_sitl_default/rootfs/log/2026-05-14/11_10_00.ulg

已理解：

.ulg 是 PX4 飞行日志
可以用于后续轨迹、姿态、速度、控制量分析
后续可用 Flight Review 或 pyulog 分析
五、当前成果

本阶段已经完成以下成果：

1. WSL Ubuntu 开发环境
2. GitHub 学习仓库
3. Linux 基础命令笔记
4. C++ / CMake / Python 测试项目
5. PX4-Autopilot 源码环境
6. PX4 SITL 编译成功
7. Gazebo Sim 8.11.0 安装成功
8. PX4 + Gazebo x500 仿真启动成功
9. PX4 shell 基础命令练习
10. PX4 .ulg 日志路径确认
11. 第一批环境搭建文档与笔记
六、当前问题
1. QGroundControl 连接仍不稳定

当前问题：

PX4 仍提示 No connection to the GCS

后续需要继续排查：

WSL2 与 Windows UDP 通信
QGroundControl Comm Link 设置
Windows 防火墙
PX4 MAVLink broadcast 参数
mavlink status 输出
2. 航点任务尚未真正完成

由于 QGroundControl 连接仍未稳定，简单航点任务还没有完整执行。

后续需要在 QGC 连接成功后完成：

Plan
Upload Mission
Arm
Start Mission
Observe Waypoints
Land
3. 飞控理论还需要系统补充

当前主要完成的是环境搭建和仿真启动。后续需要系统学习：

四旋翼动力学
PID 控制
姿态控制
位置控制
状态估计
MAVLink
Offboard 控制
七、阶段总结

本阶段最大的成果是：从零完成了无人机飞控学习环境的搭建，并成功启动 PX4 SITL + Gazebo x500 仿真。

我已经不再只是看教程，而是完成了真实飞控仿真系统的基础运行：

PX4 飞控程序
Gazebo 虚拟无人机
x500 多旋翼模型
PX4 shell
飞行日志
学习仓库

这说明我已经具备继续学习 PX4 飞控系统、MAVLink 通信、QGroundControl 地面站、航点任务和飞控算法的基础条件。

八、下一阶段计划

下一阶段重点是：

1. 彻底解决 QGroundControl 连接问题
2. 完成一次 Arm / Takeoff / Land
3. 完成一次简单航点任务
4. 学习飞行日志分析
5. 学习 MAVLink / MAVSDK
6. 开始 C++ PID 控制仿真实验

建议下一阶段任务顺序：

Day 15：排查 QGroundControl 与 WSL2 MAVLink 连接
Day 16：完成仿真起飞和降落
Day 17：完成简单航点任务
Day 18：导出并查看飞行日志
Day 19：学习 PX4 日志中的位置、速度、姿态数据
Day 20：开始 C++ PID 高度控制仿真
九、阶段反思

这两周最大的收获是：

1. 飞控学习不是只看理论，必须先跑通系统
2. PX4 环境配置涉及 Git、CMake、Python、Gazebo、OpenCV、网络等多个环节
3. 每一个报错都可以变成环境搭建经验
4. Git 仓库和阶段记录能帮助自己持续沉淀
5. 后续应该从“能跑”逐步转向“能分析、能控制、能改代码”

当前我已经完成第一阶段目标：

成功搭建 PX4 SITL + Gazebo 仿真环境。
