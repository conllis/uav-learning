# PID 实验记录 01：一维高度控制仿真

## 一、实验目的

本实验的目标是使用 C++ 实现一个 PID 控制器，并将其应用于一维高度控制仿真中，观察不同 PID 参数对高度响应的影响。

通过本实验，我希望理解：

1. PID 控制器的基本结构
2. `kp`、`ki`、`kd` 对系统响应的影响
3. 高度误差如何转化为控制输出
4. 推力、加速度、速度、高度之间的关系
5. 如何通过曲线分析控制器性能

---

## 二、实验背景

无人机高度控制的目标是让无人机高度接近期望高度。

本实验中设置：

```text
目标高度：10 m
初始高度：0 m
无人机质量：1.5 kg
重力加速度：9.81 m/s²
仿真时间：20 s
控制周期：0.01 s
实验采用简化的一维高度模型，不考虑姿态、空气阻力、电机动态和传感器噪声。

三、工程结构

实验工程位于：

code/cpp/day18_altitude_control_sim

主要文件结构：

day18_altitude_control_sim/
├── CMakeLists.txt
├── include/
│   ├── pid_controller.hpp
│   └── altitude_simulator.hpp
└── src/
    ├── pid_controller.cpp
    ├── altitude_simulator.cpp
    └── main.cpp

其中：

PIDController：负责根据高度误差计算期望加速度
AltitudeSimulator：负责根据推力、重力和质量更新高度状态
main.cpp：负责组织仿真实验并保存 CSV 数据
四、PID 控制器原理

PID 控制器根据目标值和测量值之间的误差计算控制输出。

误差定义为：

error = setpoint - measurement

PID 输出为：

output = kp * error + ki * integral + kd * derivative

其中：

P：比例项，反映当前误差
I：积分项，反映历史误差累计
D：微分项，反映误差变化速度

在本实验中：

setpoint = 目标高度
measurement = 当前高度
output = 期望垂直加速度
五、高度动力学模型

本实验不是直接修改高度，而是通过推力影响加速度，再由加速度积分得到速度，由速度积分得到高度。

核心数学关系：

error = target_altitude - altitude

a_cmd = PID(error)

T = m(g + a_cmd)

a = (T - mg) / m

v = v + a * dt

h = h + v * dt

其中：

T：推力
m：质量
g：重力加速度
a_cmd：PID 输出的期望加速度
a：实际加速度
v：垂直速度
h：高度
dt：控制周期

这说明：

PID 不直接改变高度。
PID 输出影响推力。
推力影响加速度。
加速度积分得到速度。
速度积分得到高度。
六、代码模块说明
1. PIDController

PIDController 类负责实现 PID 控制算法。

主要接口：

PIDController(double kp, double ki, double kd);

double update(double setpoint, double measurement, double dt);

void reset();

void setOutputLimits(double min_output, double max_output);

void setIntegralLimits(double min_integral, double max_integral);

其中：

update() 是核心函数，每个控制周期调用一次
setOutputLimits() 用于限制 PID 输出
setIntegralLimits() 用于防止积分饱和
reset() 用于重新开始实验
2. AltitudeSimulator

AltitudeSimulator 类负责模拟一维高度方向运动。

它保存当前状态：

altitude：高度
velocity：速度
acceleration：加速度
thrust：推力

核心更新逻辑：

根据 PID 输出计算推力
根据推力和重力计算加速度
根据加速度更新速度
根据速度更新高度
3. main.cpp

main.cpp 负责：

读取 PID 参数
创建 PID 控制器
创建高度仿真器
运行 20 秒仿真
保存 CSV 数据

CSV 输出字段：

time,setpoint,altitude,velocity,acceleration,thrust,error,kp,ki,kd
七、实验命令
1. 编译 C++ 仿真程序
cd ~/uav-learning/code/cpp/day18_altitude_control_sim

cmake -S . -B build
cmake --build build
2. 运行单组 PID 参数
./build/day18_altitude_control_sim 2.0 0.4 1.2 altitude_control_result.csv

其中：

kp = 2.0
ki = 0.4
kd = 1.2
3. 运行多组 PID 参数实验
cd ~/uav-learning/code/python/day20_pid_tuning

python3 run_pid_experiments.py
4. 绘制对比曲线
python3 plot_pid_comparison.py
八、实验参数组

本实验对比了以下 5 组 PID 参数：

p_only_low:
kp = 1.0, ki = 0.0, kd = 0.0

p_only_high:
kp = 3.0, ki = 0.0, kd = 0.0

pd_control:
kp = 2.0, ki = 0.0, kd = 1.2

pid_moderate:
kp = 2.0, ki = 0.4, kd = 1.2

pid_high_i:
kp = 2.0, ki = 1.2, kd = 1.2
九、实验输出

实验数据保存位置：

data/day20/

主要 CSV 文件：

p_only_low.csv
p_only_high.csv
pd_control.csv
pid_moderate.csv
pid_high_i.csv

曲线图片保存位置：

figures/day20/

主要图片：

pid_altitude_comparison.png
pid_error_comparison.png
pid_thrust_comparison.png
十、曲线分析方法

分析高度响应曲线时，主要观察以下指标：

1. 响应速度

高度从 0 m 接近 10 m 所需时间。

响应越快，说明控制器越积极。

2. 超调

如果目标高度是 10 m，而实际高度超过 10 m，则超过部分称为超调。

例如：

最大高度 = 11 m
目标高度 = 10 m
超调 = 1 m

超调过大说明控制器过于激进。

3. 稳态误差

仿真结束时，最终高度和目标高度之间的差值。

例如：

最终高度 = 9.8 m
目标高度 = 10 m
稳态误差 = 0.2 m
4. 震荡

如果高度在目标高度附近上下反复波动，说明系统存在震荡。

5. 推力变化

推力曲线反映控制输出是否平滑。

如果推力剧烈变化，说明控制器可能过于激进。

十一、不同参数现象分析
1. p_only_low

参数：

kp = 1.0, ki = 0.0, kd = 0.0

现象：

响应较慢
控制较温和
可能存在较明显稳态误差

理解：

kp 较小，控制器对误差反应不够强烈。
2. p_only_high

参数：

kp = 3.0, ki = 0.0, kd = 0.0

现象：

响应更快
可能出现超调
可能出现震荡

理解：

kp 增大后，系统更快接近目标，但容易冲过头。
3. pd_control

参数：

kp = 2.0, ki = 0.0, kd = 1.2

现象：

比纯 P 控制更平稳
超调可能减小
但可能仍有稳态误差

理解：

kd 提供类似“刹车”的作用，可以抑制误差快速变化。
4. pid_moderate

参数：

kp = 2.0, ki = 0.4, kd = 1.2

现象：

响应速度适中
超调较可控
稳态误差较小

理解：

适当的 ki 可以帮助消除长期误差，kd 可以抑制超调。
5. pid_high_i

参数：

kp = 2.0, ki = 1.2, kd = 1.2

现象：

积分作用更强
可能更快消除误差
但也可能导致超调和震荡

理解：

ki 过大时，积分项会积累过多，导致积分饱和和过冲。
十二、实验结论

通过本实验可以得到以下结论：

1. kp 主要影响响应速度
2. kp 过大容易导致超调和震荡
3. kd 可以抑制超调，使响应更平稳
4. ki 可以减小稳态误差
5. ki 过大容易导致积分饱和和超调
6. PID 调参应该按照 P → PD → PID 的顺序进行

推荐调参流程：

先调 kp，让系统能快速响应
再加 kd，抑制超调和震荡
最后加 ki，消除稳态误差
十三、实验反思

本实验的高度模型仍然是简化模型，和真实无人机存在差异。

当前模型没有考虑：

电机响应延迟
空气阻力
姿态变化
传感器噪声
推力非线性
电池电压变化
多旋翼姿态与高度耦合

但它仍然有价值，因为它清晰展示了：

PID 参数如何影响高度响应
控制输出如何通过动力学改变高度
为什么需要看曲线而不是只看最终数值
十四、与 PX4 学习的关系

PX4 中的高度控制、速度控制、位置控制、姿态控制都包含类似思想。

本实验对应 PX4 控制链路中的一部分：

高度误差
↓
期望加速度 / 推力
↓
无人机运动状态变化

后续学习 PX4 源码时，可以重点关注：

位置控制器
速度控制器
加速度到推力的转换
控制器参数
日志中的 setpoint 和 estimate
十五、下一步计划

下一步可以继续：

1. 自动计算上升时间、超调、稳态误差
2. 加入速度阻尼或空气阻力
3. 加入传感器噪声
4. 对比 P、PI、PD、PID 控制效果
5. 使用 Python 画更详细的响应曲线
6. 开始学习 PX4 中的 multicopter position controller
十六、本次实验总结

本次 PID 高度控制实验完成了从控制器实现、动力学仿真、参数实验到曲线分析的完整流程。

这标志着学习从“搭建环境”和“运行 PX4”进一步进入到“理解飞控控制算法”的阶段。
