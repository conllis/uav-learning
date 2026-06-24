# 第 3 个月第 1 周总结：ROS2 基础实操

## 1. 本周目标

本周目标是掌握 ROS2 的最小工程闭环：

- 创建 ROS2 workspace
- 创建 Python package
- 编写 publisher 节点
- 编写 subscriber 节点
- 发布和订阅模拟无人机高度
- 发布和订阅模拟姿态 roll / pitch / yaw
- 使用 rosbag2 记录和回放 ROS2 topic

本周的核心不是深入 ROS2 底层源码，而是建立后续 MAVSDK + ROS2 桥接所需的通信基础。

---

## 2. 本周完成内容

### Day 59：ROS2 workspace 准备

完成内容：

- 创建 `~/uav-learning/ros2_ws/src`
- 确认 `ros2` 命令可用
- 理解 workspace 和 src 的作用

workspace 结构：

```text
ros2_ws/
├── src/
├── build/
├── install/
└── log/

理解：

src：放源码 package
build：编译过程目录
install：编译安装结果，ROS2 运行节点时会从这里查找包
log：编译日志
Day 60：创建 ROS2 Python package

创建 package：

cd ~/uav-learning/ros2_ws/src
ros2 pkg create uav_ros2_basic --build-type ament_python --dependencies rclpy std_msgs

生成的包：

uav_ros2_basic/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
├── test/
└── uav_ros2_basic/

理解：

package.xml：描述包信息和依赖
setup.py：注册 Python 节点入口
uav_ros2_basic/：存放 Python 节点代码
rclpy：Python 编写 ROS2 节点的库
std_msgs：ROS2 常用标准消息包
Day 61：高度 Publisher

完成节点：

altitude_publisher.py

发布 topic：

/uav/relative_altitude

消息类型：

std_msgs/msg/Float32

运行命令：

ros2 run uav_ros2_basic altitude_publisher

功能：

每秒发布一次模拟无人机相对高度。

Day 62：高度 Subscriber

完成节点：

altitude_subscriber.py

订阅 topic：

/uav/relative_altitude

运行命令：

ros2 run uav_ros2_basic altitude_subscriber

功能：

接收高度数据并打印。

本实验验证了 ROS2 中最基本的通信关系：

altitude_publisher
    ↓
/uav/relative_altitude
    ↓
altitude_subscriber
Day 63：模拟姿态 roll / pitch / yaw

完成节点：

attitude_publisher.py
attitude_subscriber.py

发布 topic：

/uav/roll
/uav/pitch
/uav/yaw

消息类型：

std_msgs/msg/Float32

功能：

模拟无人机姿态角变化，并通过 ROS2 topic 发布。

Day 64：rosbag2 记录与回放

记录命令：

ros2 bag record -o data/month3/rosbag_attitude /uav/roll /uav/pitch /uav/yaw

查看信息：

ros2 bag info data/month3/rosbag_attitude

回放：

ros2 bag play data/month3/rosbag_attitude

理解：

rosbag2 可以把 ROS2 topic 数据记录下来，之后用于回放、调试、复现实验和离线分析。

3. ROS2 workspace 是什么？

ROS2 workspace 是 ROS2 项目的工作区。

本项目中 workspace 是：

~/uav-learning/ros2_ws

它用于统一管理多个 ROS2 package。

最重要的是 src 目录，因为自己写的 ROS2 package 都放在这里。

4. package 是什么？

package 是 ROS2 中的功能模块。

一个 package 可以包含多个节点、配置文件、launch 文件和依赖说明。

本周创建的 package 是：

uav_ros2_basic

它用于存放 ROS2 基础练习节点。

5. node 是什么？

node 是 ROS2 中独立运行的程序。

本周创建的节点包括：

altitude_publisher
altitude_subscriber
attitude_publisher
attitude_subscriber

每个节点负责一个相对独立的功能。

ROS2 推荐把复杂系统拆成多个节点，而不是写成一个巨大程序。

6. topic 是什么？

topic 是 ROS2 节点之间传递消息的通道。

例如：

/uav/relative_altitude
/uav/roll
/uav/pitch
/uav/yaw

Publisher 往 topic 发布数据，Subscriber 从 topic 接收数据。

Publisher 和 Subscriber 不需要直接互相调用，只需要使用相同的 topic 名称和消息类型。

7. publisher / subscriber 怎么通信？

通信关系可以理解为：

Publisher
    ↓ publish
Topic
    ↓ subscribe
Subscriber

本周高度通信实验：

altitude_publisher
    ↓
/uav/relative_altitude
    ↓
altitude_subscriber

姿态通信实验：

attitude_publisher
    ↓
/uav/roll
/uav/pitch
/uav/yaw
    ↓
attitude_subscriber

这种机制让系统解耦。后续 MAVSDK 节点可以只负责发布 PX4 telemetry，日志节点或控制节点只需要订阅对应 topic。

8. rosbag 有什么用？

rosbag2 是 ROS2 的数据记录和回放工具。

它的作用包括：

记录 ROS2 topic 数据
回放实验过程
离线分析无人机状态
复现问题
为后续画曲线和写报告提供数据

在无人机项目中，rosbag2 可以记录：

高度
姿态
位置
速度
控制命令
任务阶段

这对调试 Offboard、分析轨迹误差非常重要。

9. ROS2 和 MAVSDK 有什么区别？

ROS2 是机器人系统通信框架。

它主要负责：

节点组织
topic 通信
service/action
数据记录
多模块协作

MAVSDK 是 MAVLink 的高级接口库。

它主要负责：

连接 PX4
读取 telemetry
发送 takeoff / land / goto 等命令
执行 offboard setpoint 控制

两者关系：

PX4 SITL
    ↓
MAVSDK 读取 telemetry / 发送命令
    ↓
ROS2 节点发布 topic / 订阅 command
    ↓
其他 ROS2 节点记录、分析、控制

所以，ROS2 更像系统组织框架，MAVSDK 更像 PX4 控制接口。

10. 本周最大收获

本周最大的收获是跑通了 ROS2 最小通信闭环：

Python 节点
    ↓
Publisher
    ↓
Topic
    ↓
Subscriber

并初步掌握了 rosbag2 的记录和回放。

这为第 2 周的 ROS2 + MAVSDK 桥接打下基础。

11. 当前不足

目前还没有接入真实 PX4 telemetry。

目前发布的高度和姿态都是模拟数据。

还没有把 ROS2 topic 保存成 CSV。

还没有通过 ROS2 topic 触发 MAVSDK Action。

这些会在第 2 周继续完成。

12. 下周计划

第 2 周目标是完成 ROS2 + MAVSDK 桥接：

创建 uav_mavsdk_bridge package
用 MAVSDK 连接 PX4 SITL
把 PX4 telemetry 发布成 ROS2 topic
写 ROS2 subscriber 保存 telemetry CSV
通过 /uav/action_command 触发 MAVSDK Action
实现 ROS2 topic 控制 PX4 起飞和降落

---

# 3. 把本周代码结构也记录下来

执行：

```bash
cd ~/uav-learning
tree -L 4 -I "build|install|log|__pycache__|venv" ros2_ws/src/uav_ros2_basic

把输出复制到报告的最后，作为第 1 周证据。

4. 今日完成标准

今天完成后，你应该有：

reports/month3/week1_ros2_basic_summary.md

并且报告里回答了这 7 个问题：

1. ROS2 workspace 是什么？
2. package 是什么？
3. node 是什么？
4. topic 是什么？
5. publisher / subscriber 怎么通信？
6. rosbag 有什么用？
7. ROS2 和 MAVSDK 有什么区别？
