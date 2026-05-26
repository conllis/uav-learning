// 作用：
// 定义坐标系转换工具函数。
// 本文件只放函数声明，不放具体实现。
// 具体实现写在 src/coordinate_utils.cpp 中。
//
// 本项目练习的坐标系：
// 1. NED: North-East-Down，PX4 常用世界坐标系
// 2. ENU: East-North-Up，ROS 常用世界坐标系
// 3. FRD: Forward-Right-Down，PX4 常用机体系
// 4. FLU: Forward-Left-Up，ROS 常用机体系

#pragma once

#include <array>

// 三维向量类型。
// data[0] 表示 x
// data[1] 表示 y
// data[2] 表示 z
using Vector3 = std::array<double, 3>;

// 角度转弧度。
// C++ 的 sin/cos 函数使用弧度。
double degToRad(double degree);

// NED 转 ENU。
// NED: x=north, y=east, z=down
// ENU: x=east,  y=north, z=up
Vector3 nedToEnu(const Vector3& ned);

// ENU 转 NED。
// 公式和 NED 转 ENU 形式类似。
Vector3 enuToNed(const Vector3& enu);

// FRD 转 FLU。
// FRD: x=forward, y=right, z=down
// FLU: x=forward, y=left,  z=up
Vector3 frdToFlu(const Vector3& frd);

// FLU 转 FRD。
Vector3 fluToFrd(const Vector3& flu);

// 根据 yaw 角，把机体系 FRD 中的水平速度转换到 NED 世界系。
// 输入：
// body_velocity_frd: 机体系速度，x 前、y 右、z 下
// yaw_rad: 无人机相对于 NED 世界系的偏航角，单位弧度
//
// 输出：
// NED 世界系速度，x 北、y 东、z 下
Vector3 bodyFrdVelocityToNed(const Vector3& body_velocity_frd, double yaw_rad);

// 打印向量，方便观察结果。
void printVector(const char* name, const Vector3& vector);
