# Day 18 写高度控制仿真

## 今日目标

在 Day 17 PIDController 的基础上，写一个简化的一维高度控制仿真。

---

## 1. 工程结构

```text
day18_altitude_control_sim/
├── CMakeLists.txt
├── include/
│   ├── pid_controller.hpp
│   └── altitude_simulator.hpp
└── src/
    ├── pid_controller.cpp
    ├── altitude_simulator.cpp
    └── main.cpp
2. 控制思路
目标高度
↓
当前高度
↓
计算误差
↓
PID 输出期望加速度
↓
转换为推力
↓
更新加速度、速度、高度
3. 数学模型
error = target_altitude - altitude

acceleration_command = PID(error)

thrust = mass * (gravity + acceleration_command)

acceleration = (thrust - mass * gravity) / mass

velocity = velocity + acceleration * dt

altitude = altitude + velocity * dt
4. 参数
mass = 1.5 kg
gravity = 9.81 m/s^2
target_altitude = 10 m
dt = 0.01 s
simulation_time = 20 s
5. 编译运行
cd ~/uav-learning/code/cpp/day18_altitude_control_sim
cmake -S . -B build
cmake --build build
./build/day18_altitude_control_sim
6. 输出文件
altitude_control_result.csv

字段：

time,setpoint,altitude,velocity,acceleration,thrust,error
7. 今日理解
PID 控制器负责根据高度误差计算期望加速度
高度仿真器负责根据推力和重力更新运动状态
thrust = mass * (gravity + acceleration_command)
acceleration = (thrust - mass * gravity) / mass
高度通过速度积分得到，速度通过加速度积分得到
8. 今日总结

今天完成了一个一维高度控制仿真。相比 Day 17，这次引入了质量、重力、推力、加速度和速度，更接近真实无人机高度控制问题。

这个仿真后续可以用于 PID 参数整定、结果画图和飞控控制原理理解。


---

# 十五、提交 Day 18
