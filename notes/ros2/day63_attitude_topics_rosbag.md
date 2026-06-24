# Day 63 发布模拟姿态 roll / pitch / yaw 与 rosbag2 记录

## 今日目标

发布模拟无人机姿态数据，并使用 rosbag2 记录和回放 ROS2 topic。

## 今日话题

| Topic | Message |
|---|---|
| /uav/roll | std_msgs/msg/Float32 |
| /uav/pitch | std_msgs/msg/Float32 |
| /uav/yaw | std_msgs/msg/Float32 |

## 节点

### attitude_publisher

功能：每 0.5 秒发布一次模拟 roll、pitch、yaw。

运行：

```bash
ros2 run uav_ros2_basic attitude_publisher
attitude_subscriber

功能：订阅 /uav/roll、/uav/pitch、/uav/yaw，并打印姿态数据。

运行：

ros2 run uav_ros2_basic attitude_subscriber
rosbag2 记录

记录命令：

ros2 bag record -o data/month3/rosbag_attitude /uav/roll /uav/pitch /uav/yaw

查看信息：

ros2 bag info data/month3/rosbag_attitude

回放：

ros2 bag play data/month3/rosbag_attitude
今日理解

Publisher 负责发布姿态数据。

Subscriber 负责接收姿态数据。

Topic 是节点之间的数据通道。

rosbag2 可以把 topic 数据记录下来，之后再回放，用于调试、复现实验和离线分析。

今日结果
attitude_publisher 是否成功运行：
attitude_subscriber 是否成功接收：
/uav/roll 是否能 echo：
/uav/pitch 是否能 echo：
/uav/yaw 是否能 echo：
rosbag 是否成功记录：
rosbag 是否成功回放：
遇到的问题：

---

# 今日完成标准

今天完成后，你应该满足：

```text
1. attitude_publisher.py 写完
2. attitude_subscriber.py 写完
3. setup.py 已注册两个节点
4. colcon build 成功
5. ros2 run uav_ros2_basic attitude_publisher 能运行
6. ros2 run uav_ros2_basic attitude_subscriber 能收到数据
7. ros2 topic echo /uav/roll 能看到数据
8. ros2 bag record 能记录三个姿态话题
9. ros2 bag info 能查看 bag 信息
10. ros2 bag play 能回放数据
