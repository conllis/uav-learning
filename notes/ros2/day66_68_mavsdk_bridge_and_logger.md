# Day 66-68 ROS2 + MAVSDK telemetry bridge and CSV logger

## 今日目标

创建 `uav_mavsdk_bridge` 包，用 MAVSDK 连接 PX4 SITL，读取 telemetry，并发布成 ROS2 topic。随后用 ROS2 subscriber 订阅 telemetry topic，并保存为 CSV。

## ROS2 package

包名：

```text
uav_mavsdk_bridge

创建命令：

cd ~/uav-learning/ros2_ws/src
ros2 pkg create uav_mavsdk_bridge --build-type ament_python --dependencies rclpy std_msgs geometry_msgs
节点
px4_telemetry_bridge

功能：

MAVSDK 连接 PX4 SITL
读取 relative altitude
读取 roll / pitch / yaw
读取 flight mode
发布成 ROS2 topic
px4_telemetry_logger

功能：

订阅 PX4 telemetry topic
保存 CSV 文件
Topic
Topic	Message
/px4/relative_altitude	std_msgs/msg/Float32
/px4/roll	std_msgs/msg/Float32
/px4/pitch	std_msgs/msg/Float32
/px4/yaw	std_msgs/msg/Float32
/px4/flight_mode	std_msgs/msg/String
CSV 输出
~/uav-learning/data/month3/ros2_px4_telemetry.csv

字段：

time_sec, relative_altitude_m, roll_deg, pitch_deg, yaw_deg, flight_mode
今日理解

MAVSDK 负责连接 PX4 并读取真实 telemetry。

ROS2 负责把 telemetry 组织成 topic，供其他节点订阅。

bridge 节点的作用是把 PX4/MAVSDK 世界的数据转成 ROS2 世界的数据。

logger 节点不直接连接 PX4，只订阅 ROS2 topic，因此它和 PX4 解耦。

今日结果
PX4 SITL 是否启动成功：
MAVSDK 是否连接成功：
/px4/relative_altitude 是否有数据：
/px4/roll 是否有数据：
/px4/pitch 是否有数据：
/px4/yaw 是否有数据：
CSV 是否生成：
遇到的问题：

---

# 13. 今日完成标准

今天完成后，你应该满足：

```text
1. uav_mavsdk_bridge 包创建成功
2. px4_telemetry_bridge.py 写完
3. px4_telemetry_logger.py 写完
4. setup.py 注册两个节点
5. colcon build 成功
6. PX4 SITL 正常运行
7. MAVSDK 能连接 PX4
8. ROS2 topic 能看到 /px4/relative_altitude、/px4/roll、/px4/pitch、/px4/yaw
9. CSV 文件 data/month3/ros2_px4_telemetry.csv 生成并有数据
14. 常见问题

如果 bridge 一直停在：

Connecting to PX4 via udp://:14540 ...

先确认 PX4 SITL 已经启动，再尝试把代码里的：

CONNECTION_URL = "udp://:14540"

改成：

CONNECTION_URL = "udpin://0.0.0.0:14540"

然后重新编译：

cd ~/uav-learning/ros2_ws
colcon build --packages-select uav_mavsdk_bridge
source install/setup.bash

如果 ros2 run 找不到节点，检查：

source ~/uav-learning/ros2_ws/install/setup.bash

以及 setup.py 里的 console_scripts 是否写对。

如果 CSV 没有数据，先检查 bridge 是否在发布：

ros2 topic echo /px4/relative_altitude

只要这个没有数据，logger 就不会写入有效行。
