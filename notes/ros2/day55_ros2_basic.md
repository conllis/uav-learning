# Day 55 ROS2 入门

## 今日目标

今天学习 ROS2 的基础概念，并完成 ROS2 安装验证。

今日目标包括：

```text
1. 确认 Ubuntu 版本
2. 安装对应版本 ROS2
3. 验证 ros2 命令可用
4. 理解 Node、Topic、Message、Publisher、Subscriber、Service、Action
5. 理解 ROS2 和 MAVSDK 的区别
```

---

## 1. ROS2 是什么

ROS2 是机器人软件开发框架。

它的核心作用不是直接控制电机，而是让机器人系统里的多个程序能够有组织地通信和协作。

一句话理解：

```text
ROS2 是机器人系统中的通信和组织框架。
```

---

## 2. 为什么无人机要学 ROS2

无人机系统通常包含多个模块：

```text
相机模块
识别模块
定位模块
规划模块
控制模块
记录模块
可视化模块
```

ROS2 可以让这些模块通过统一方式通信。

例如：

```text
相机节点发布图像
识别节点订阅图像并发布目标位置
规划节点根据目标位置生成轨迹
控制节点根据轨迹发送控制目标
记录节点保存飞行数据
```

---

## 3. Node 节点

Node 是 ROS2 中的一个独立程序。

例如：

```text
camera_node
detect_node
planner_node
control_node
logger_node
```

一句话理解：

```text
Node = 负责某个功能的小程序。
```

---

## 4. Topic 话题

Topic 是节点之间持续传递数据的通道。

例如：

```text
/camera/image
/drone/position
/drone/attitude
/target/position
/control/setpoint
```

一句话理解：

```text
Topic = 节点之间传数据的通道。
```

---

## 5. Message 消息

Message 是 Topic 中传输的数据格式。

例如位置消息可能包含：

```text
x
y
z
timestamp
```

姿态消息可能包含：

```text
roll
pitch
yaw
```

一句话理解：

```text
Message = Topic 中传输的数据内容和格式。
```

---

## 6. Publisher 发布者

Publisher 是发送消息的一方。

例如：

```text
定位节点发布无人机位置
相机节点发布图像
控制节点发布目标 setpoint
```

一句话理解：

```text
Publisher = 发消息的节点。
```

---

## 7. Subscriber 订阅者

Subscriber 是接收消息的一方。

例如：

```text
控制节点订阅无人机位置
识别节点订阅相机图像
日志节点订阅 telemetry
```

一句话理解：

```text
Subscriber = 收消息的节点。
```

---

## 8. Service 服务

Service 是一问一答式通信。

例如：

```text
请求保存地图 → 返回保存成功
请求切换模式 → 返回切换结果
请求查询参数 → 返回参数值
```

一句话理解：

```text
Service = 请求一次，返回一次结果。
```

---

## 9. ROS2 Action 动作

ROS2 Action 适合耗时任务。

例如：

```text
导航到某个点
执行一段轨迹
完成一次巡检任务
```

它可以：

```text
启动任务
反馈进度
返回结果
取消任务
```

注意：

```text
ROS2 Action 和 MAVSDK Action 不是同一个东西。
```

MAVSDK Action 是：

```text
arm
takeoff
land
return_to_launch
```

ROS2 Action 是：

```text
适合长期任务的通信机制。
```

---

## 10. ROS2 和 MAVSDK 的区别

MAVSDK 更像是直接和 PX4 通信的工具库。

ROS2 更像是组织整个机器人系统的软件框架。

对比：

```text
MAVSDK：适合写简单程序连接 PX4、读取 telemetry、发送控制命令
ROS2：适合组织多个模块协作，如感知、定位、规划、控制和记录
```

---

## 11. ROS2 在无人机项目中的结构

无人机巡检项目可以拆成：

```text
camera_node：发布图像
detect_node：识别目标
localization_node：发布无人机位置
planner_node：生成轨迹
control_node：发送控制目标
logger_node：保存日志
```

这些节点通过 Topic、Service、Action 通信。

---

## 12. 常用 ROS2 命令

查看 ROS2 是否可用：

```bash
ros2 --help
```

查看节点：

```bash
ros2 node list
```

查看话题：

```bash
ros2 topic list
```

查看话题数据：

```bash
ros2 topic echo /topic_name
```

查看话题信息：

```bash
ros2 topic info /topic_name
```

查看消息格式：

```bash
ros2 interface show geometry_msgs/msg/Twist
```

---

## 13. 安装验证记录

Ubuntu 版本：

```text
____
```

ROS2 版本：

```text
humble / jazzy
```

`ros2 --help` 是否成功：

```text
是 / 否：
```

`echo $ROS_DISTRO` 输出：

```text
____
```

talker / listener 是否通信成功：

```text
是 / 否：
```

---

## 14. 今日总结

今天理解了 ROS2 的基础概念。

最重要的结论：

```text
ROS2 不是单独控制无人机的工具，而是组织机器人系统中多个模块通信和协作的框架。
```

一句话总结：

```text
Day 55 的核心是理解 ROS2 的节点、话题、消息、发布订阅机制，以及它在无人机系统中的作用。
```
