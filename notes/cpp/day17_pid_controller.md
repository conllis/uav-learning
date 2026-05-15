# Day 17 写一个 PID 控制器类

## 今日目标

实现一个 C++ PIDController 类，并用一个简化高度控制仿真测试它。

---

## 1. PID 基本公式

```text
error = setpoint - measurement

P = kp * error
I = ki * integral(error)
D = kd * derivative(error)

output = P + I + D
2. PID 三个参数
kp

比例项。误差越大，输出越大。

ki

积分项。用于消除长期误差。

kd

微分项。用于抑制误差变化速度，减少过冲。

3. 工程结构
day17_pid_controller/
├── CMakeLists.txt
├── include/
│   └── pid_controller.hpp
└── src/
    ├── pid_controller.cpp
    └── main.cpp
4. 编译运行
cd ~/uav-learning/code/cpp/day17_pid_controller
cmake -S . -B build
cmake --build build
./build/day17_pid_controller

保存结果：

./build/day17_pid_controller > pid_result.csv
5. 今日实现的类
class PIDController {
public:
    PIDController(double kp, double ki, double kd);

    double update(double setpoint, double measurement, double dt);

    void reset();

    void setGains(double kp, double ki, double kd);
    void setOutputLimits(double min_output, double max_output);
    void setIntegralLimits(double min_integral, double max_integral);
};
6. 输出限制

真实系统的执行器能力有限，所以 PID 输出不能无限大。

示例：

altitude_pid.setOutputLimits(-3.0, 3.0);
7. 积分限制

积分项如果无限累积，可能导致积分饱和。

示例：

altitude_pid.setIntegralLimits(-10.0, 10.0);
8. 今日实验

目标高度：

10 m

初始高度：

0 m

控制周期：

dt = 0.1 s

观察结果：

高度逐渐接近目标高度，PID 控制器基本工作正常。
9. 今日总结

今天完成了第一个 C++ 控制算法类 PIDController。

我理解了：

error 是目标值和测量值的差
P 根据当前误差输出
I 根据历史误差输出
D 根据误差变化速度输出
dt 是控制周期
输出限制模拟执行器能力
积分限制用于防止积分饱和

这个 PIDController 后续可以扩展为高度控制、速度控制或姿态控制仿真模块。
