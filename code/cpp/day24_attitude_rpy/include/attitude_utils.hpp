// 作用：
// 定义姿态角工具函数，用于学习 roll、pitch、yaw 的基本关系。
// 本文件只放声明，不放具体实现。
// 具体函数实现写在 src/attitude_utils.cpp 中。

#pragma once

#include <array>

// 用 3x3 数组表示旋转矩阵。
// Matrix3 的含义：
// matrix[row][col]
using Matrix3 = std::array<std::array<double, 3>, 3>;

// 用 3 维数组表示向量。
// 例如 thrust direction = {x, y, z}
using Vector3 = std::array<double, 3>;

// 角度转弧度。
// C++ 的 sin/cos 函数使用弧度，而不是角度。
double degToRad(double degree);

// 根据 roll、pitch、yaw 生成旋转矩阵。
// 输入单位：弧度。
// 这里采用常见的 Z-Y-X 顺序：
// yaw -> pitch -> roll
Matrix3 eulerToRotationMatrix(double roll, double pitch, double yaw);

// 矩阵乘以向量。
// 用于计算机体坐标系中的向量旋转到世界坐标系后的方向。
Vector3 multiply(const Matrix3& matrix, const Vector3& vector);

// 打印 3x3 矩阵。
void printMatrix(const Matrix3& matrix);

// 打印 3 维向量。
void printVector(const Vector3& vector);
