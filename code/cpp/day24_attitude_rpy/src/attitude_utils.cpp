// 作用：
// 实现姿态角工具函数。
// 主要包括：
// 1. 角度转弧度
// 2. roll/pitch/yaw 转旋转矩阵
// 3. 矩阵和向量相乘
// 4. 打印矩阵和向量

#include "attitude_utils.hpp"

#include <cmath>
#include <iomanip>
#include <iostream>

double degToRad(double degree) {
    // 角度转弧度公式：
    // rad = degree * pi / 180
    return degree * M_PI / 180.0;
}

Matrix3 eulerToRotationMatrix(double roll, double pitch, double yaw) {
    // roll  绕 X 轴旋转
    // pitch 绕 Y 轴旋转
    // yaw   绕 Z 轴旋转

    const double cr = std::cos(roll);
    const double sr = std::sin(roll);

    const double cp = std::cos(pitch);
    const double sp = std::sin(pitch);

    const double cy = std::cos(yaw);
    const double sy = std::sin(yaw);

    // 采用 Z-Y-X 欧拉角顺序：
    // R = Rz(yaw) * Ry(pitch) * Rx(roll)
    //
    // 注意：
    // 不同教材和飞控系统可能采用不同坐标系和旋转约定。
    // 今天这个矩阵主要用于理解 roll/pitch/yaw 对方向的影响。
    Matrix3 rotation = {{
        {cy * cp, cy * sp * sr - sy * cr, cy * sp * cr + sy * sr},
        {sy * cp, sy * sp * sr + cy * cr, sy * sp * cr - cy * sr},
        {-sp,     cp * sr,                 cp * cr}
    }};

    return rotation;
}

Vector3 multiply(const Matrix3& matrix, const Vector3& vector) {
    Vector3 result{0.0, 0.0, 0.0};

    // 普通矩阵乘法：
    // result = matrix * vector
    for (int row = 0; row < 3; ++row) {
        result[row] =
            matrix[row][0] * vector[0] +
            matrix[row][1] * vector[1] +
            matrix[row][2] * vector[2];
    }

    return result;
}

void printMatrix(const Matrix3& matrix) {
    std::cout << std::fixed << std::setprecision(4);

    for (const auto& row : matrix) {
        std::cout << "[ ";
        for (double value : row) {
            std::cout << std::setw(9) << value << " ";
        }
        std::cout << "]" << std::endl;
    }
}

void printVector(const Vector3& vector) {
    std::cout << std::fixed << std::setprecision(4);

    std::cout
        << "[ "
        << vector[0] << ", "
        << vector[1] << ", "
        << vector[2]
        << " ]"
        << std::endl;
}
