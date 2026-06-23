# Day 60 ROS2 Python package + Publisher + Subscriber

## 今日目标

创建第一个 ROS2 Python package，并完成一个最小 publisher/subscriber 通信实验。

## Package

包名：

```text
uav_ros2_basic

创建命令：

cd ~/uav-learning/ros2_ws/src
ros2 pkg create uav_ros2_basic --build-type ament_python --dependencies rclpy std_msgs
Topic

话题名：

/uav/relative_altitude

消息类型：

std_msgs/msg/Float32
Publisher

节点名：

altitude_publisher

功能：

每秒发布一次模拟无人机相对高度。

运行命令：

ros2 run uav_ros2_basic altitude_publisher
Subscriber

节点名：

altitude_subscriber

功能：

订阅 /uav/relative_altitude，并打印接收到的高度。

运行命令：

ros2 run uav_ros2_basic altitude_subscriber
今日理解

Publisher 负责发布消息。

Subscriber 负责接收消息。

Topic 是消息传输通道。

Message 是消息格式。

本实验中，altitude_publisher 每秒向 /uav/relative_altitude 发布 Float32 数据，altitude_subscriber 从同一个 topic 接收并打印数据。

今日结果
package 是否创建成功：
colcon build 是否成功：
publisher 是否能运行：
subscriber 是否能收到数据：
ros2 topic echo 是否能看到数据：
遇到的问题：

---

# 10. 今日完成标准

今天完成后，你应该满足：

```text
1. uav_ros2_basic package 创建成功
2. altitude_publisher.py 写完
3. altitude_subscriber.py 写完
4. setup.py 注册了两个 console_scripts
5. colcon build 成功
6. publisher 能持续发布高度
7. subscriber 能接收高度
8. ros2 topic echo /uav/relative_altitude 能看到数据
9. day60 笔记完成
