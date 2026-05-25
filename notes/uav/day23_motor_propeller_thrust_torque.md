# Day 23 学习电机、桨叶、推力、力矩关系

## 今日目标

理解四旋翼中电机转速、桨叶推力、反扭矩和机体力矩之间的关系。

---

## 1. 电机和桨叶的作用

电机负责带动螺旋桨旋转，螺旋桨通过推动空气产生推力。

```text
电池
↓
电调 ESC
↓
电机
↓
桨叶
↓
推力
2. RPM 和角速度

电机转速常用 RPM 表示，控制建模中常用角速度 ω。

关系：

ω = RPM × 2π / 60

单位：

RPM：转 / 分钟
ω：rad/s
3. 推力模型

简化推力模型：

T = kf × ω²

其中：

T：推力
kf：推力系数
ω：角速度

含义：

推力与角速度平方近似成正比
4. 反扭矩模型

简化反扭矩模型：

Q = km × ω²

其中：

Q：反扭矩
km：力矩系数
ω：角速度

不同旋向的电机产生方向相反的反扭矩。

5. 总推力

四个电机推力：

T1, T2, T3, T4

总推力：

T_total = T1 + T2 + T3 + T4

悬停条件：

T_total = mg
6. Roll / Pitch / Yaw 来源
Roll：左右推力差
Pitch：前后推力差
Yaw：不同旋向电机的反扭矩差
7. Mixer / Control Allocation

飞控希望控制：

Throttle
Roll
Pitch
Yaw

但实际执行器是：

M1
M2
M3
M4

所以需要把控制量分配到四个电机，这叫：

Mixer / Control Allocation
8. Day 23 C++ 实验

项目路径：

code/cpp/day23_motor_thrust_torque

编译运行：

cd ~/uav-learning/code/cpp/day23_motor_thrust_torque
cmake -S . -B build
cmake --build build
./build/day23_motor_thrust_torque

实验内容：

输入四个电机 RPM
计算每个电机的角速度
计算每个电机推力
计算每个电机反扭矩
计算总推力和总 yaw 力矩
9. 今日理解

四个电机转速相同：

总推力增加
反扭矩互相抵消
不会主动偏航

一组旋向电机加速，另一组减速：

总 yaw 力矩不为 0
无人机产生偏航趋势

四个电机同时加速：

总推力增大
无人机更容易上升
今日总结

今天理解了电机、桨叶、推力和力矩的基本关系。

最重要的公式：

ω = RPM × 2π / 60
T = kf × ω²
Q = km × ω²
T_total = T1 + T2 + T3 + T4

最重要的控制理解：

高度靠总推力
Roll 靠左右推力差
Pitch 靠前后推力差
Yaw 靠反扭矩差

---

# 九、提交 Day 23
