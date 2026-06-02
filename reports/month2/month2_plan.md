# 第 2 个月学习计划：C++ 控制仿真与 PX4 Telemetry 入门

## 一、本月定位

第 1 个月已经完成了 PX4 SITL、Gazebo、QGroundControl、PID 入门、四旋翼基础和 PX4 数据流整理。

第 2 个月的目标是从“会跑 PX4 仿真”升级到“能用 C++ 写控制仿真，并能用程序读取 PX4 状态”。

本月不追求一次学完所有公司推荐课程，而是先抓住最核心的三条线：

1. C++ / CMake 工程能力；
2. 飞控算法基础，重点是 PID、高度控制、姿态控制；
3. MAVLink / MAVSDK 入门，能够读取 PX4 SITL 的 telemetry 数据。

---

## 二、本月总目标

本月结束时，我应该完成以下成果：

1. 建立一个 C++ / CMake 控制仿真项目；
2. 实现 PID 控制器类；
3. 完成一维高度 PID 控制仿真；
4. 完成 roll / pitch 单轴姿态 PID 仿真；
5. 对比不同 PID 参数下的响应效果；
6. 输出高度、姿态、推力、力矩等曲线；
7. 初步理解 MAVLink 和 MAVSDK；
8. 用 MAVSDK 连接 PX4 SITL；
9. 读取无人机高度、位置、姿态、飞行模式等 telemetry 数据；
10. 保存 telemetry 数据到 CSV；
11. 写一份第 2 个月总结报告。

---

## 三、本月项目目录

本月主要使用以下目录：

```text
uav-learning/
├── code/
│   ├── 02_cpp_quadrotor_pid_sim/
│   └── 03_mavsdk_telemetry/
├── notes/
│   ├── control/
│   ├── mavlink/
│   ├── ros2/
│   ├── sensor/
│   └── stm32/
├── reports/
│   └── month2/
├── screenshots/
│   └── month2/
└── data/
    └── month2/
```

其中：

```text
02_cpp_quadrotor_pid_sim
```

用于保存 C++ 控制仿真代码。

```text
03_mavsdk_telemetry
```

用于保存 MAVSDK 连接 PX4 并读取状态数据的代码。

---

## 四、本月每周安排

### 第 1 周：C++ / CMake + 高度 PID 仿真

目标：

1. 搭建 C++ / CMake 工程结构；
2. 实现 PIDController 类；
3. 写一维高度动力学模型；
4. 输出高度响应 CSV；
5. 用 Python 画高度响应曲线；
6. 对比不同 PID 参数效果。

本周产出：

```text
code/02_cpp_quadrotor_pid_sim/
reports/month2/week1_cpp_pid_summary.md
```

本周完成标准：

1. C++ 项目可以成功编译；
2. PID 控制器可以运行；
3. 能模拟无人机从 0 m 上升到目标高度；
4. 能画出高度响应曲线；
5. 能说明 P、I、D 参数变化对结果的影响。

---

### 第 2 周：姿态控制与级联控制理解

目标：

1. 复习 roll、pitch、yaw；
2. 理解推力和力矩的区别；
3. 学习四旋翼混控基本思想；
4. 写 roll 单轴 PID 控制仿真；
5. 写 pitch 单轴 PID 控制仿真；
6. 理解位置控制、姿态控制、角速度控制之间的级联关系。

本周产出：

```text
notes/control/day36_attitude_axes.md
notes/control/day40_cascade_control.md
reports/month2/week2_attitude_control_summary.md
```

本周完成标准：

1. 能解释高度控制和姿态控制的区别；
2. 能解释 thrust 和 torque 的区别；
3. 能解释为什么飞控需要内环和外环；
4. 能画出“位置 → 姿态 → 角速度 → 电机”的控制链路；
5. 能运行 roll / pitch 单轴姿态控制仿真。

---

### 第 3 周：MAVLink / MAVSDK 入门

目标：

1. 复习 PX4 数据流；
2. 学习 MAVLink 基本概念；
3. 学习 MAVSDK 的作用；
4. 用 MAVSDK 连接 PX4 SITL；
5. 读取无人机 telemetry 数据；
6. 保存高度、姿态、位置、飞行模式等数据到 CSV；
7. 画出 telemetry 曲线。

本周产出：

```text
code/03_mavsdk_telemetry/
notes/mavlink/day50_mavlink_basic.md
reports/month2/week3_mavsdk_telemetry_summary.md
```

本周完成标准：

1. PX4 SITL 能正常启动；
2. MAVSDK 程序能连接 PX4；
3. 能读取高度、位置、姿态、飞行模式；
4. 能保存 telemetry 数据；
5. 能画出高度和姿态变化曲线。

---

### 第 4 周：ROS2 / 传感器 / STM32 预备 + 月度总结

目标：

1. 了解 ROS2 的 node、topic、message、service、launch；
2. 了解 IMU、GPS、气压计、磁力计的基本作用；
3. 写一个简单低通滤波实验；
4. 了解 STM32、GPIO、中断、DMA、定时器、FreeRTOS 任务等概念；
5. 整理本月代码和 README；
6. 写第 2 个月总结报告。

本周产出：

```text
notes/ros2/day51_ros2_basic.md
notes/sensor/day52_sensor_basic.md
notes/stm32/day54_stm32_freertos_overview.md
reports/month2/month2_summary.md
```

本周完成标准：

1. 能说明 ROS2 在无人机系统中的作用；
2. 能说明 IMU、GPS、气压计、磁力计分别提供什么信息；
3. 能理解为什么传感器数据需要滤波；
4. 能说明 STM32 / FreeRTOS 在飞控系统中的作用；
5. 能完成第 2 个月总结报告。

---

## 五、本月每天最低标准

每天必须完成三件事：

1. 学一个明确知识点；
2. 写一点代码、跑一个实验或整理一份笔记；
3. 提交一次 Git。

每日记录模板：

```text
日期：

今日任务：
1.
2.
3.

今天完成：
1.
2.
3.

今天遇到的问题：
1.
2.

今天解决的问题：
1.
2.

还没解决的问题：
1.
2.

明天第一件事：
1.
```

---

## 六、本月重点理解的问题

本月结束前，我应该能回答以下问题：

1. C++ 项目为什么要分 include、src 和 CMakeLists.txt？
2. PID 控制器的 P、I、D 分别起什么作用？
3. 高度控制中，推力、重力、加速度、速度、高度之间是什么关系？
4. 姿态控制中，角度、角速度、力矩之间是什么关系？
5. 为什么四旋翼控制不是一个 PID，而是级联控制？
6. MAVLink 是什么？
7. MAVSDK 和 QGroundControl 的区别是什么？
8. telemetry 是什么？
9. PX4 中的当前状态和 setpoint 有什么区别？
10. 为什么后续学习 ROS2、传感器、STM32 之前，要先打好 C++ 和控制基础？

---

## 七、本月最终成果

本月结束时，应完成以下文件或项目：

```text
code/02_cpp_quadrotor_pid_sim/
code/03_mavsdk_telemetry/
reports/month2/week1_cpp_pid_summary.md
reports/month2/week2_attitude_control_summary.md
reports/month2/week3_mavsdk_telemetry_summary.md
reports/month2/month2_summary.md
notes/control/
notes/mavlink/
notes/ros2/
notes/sensor/
notes/stm32/
```

本月一句话目标：

```text
把 PX4 飞控学习从“会运行仿真”推进到“能写控制仿真、能读取飞控状态、能为 Offboard 控制做准备”。
```
