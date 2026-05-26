// 作用：
// 演示 roll、pitch、yaw 如何影响机体推力方向。
// 这个程序不是完整飞控，只是用于理解姿态角。
// 
// 思路：
// 1. 设置 roll / pitch / yaw 角度
// 2. 转成弧度
// 3. 生成旋转矩阵
// 4. 假设机体推力方向是 body_z_up
// 5. 计算姿态变化后推力方向在世界坐标中的方向

#include "attitude_utils.hpp"

#include <iostream>

int main() {
    // -----------------------------
    // 1. 设置姿态角，单位是 degree
    // -----------------------------
    // 你可以修改这里的数值，观察旋转矩阵和推力方向变化。
    const double roll_deg = 10.0;
    const double pitch_deg = -15.0;
    const double yaw_deg = 30.0;

    // -----------------------------
    // 2. 角度转弧度
    // -----------------------------
    // C++ 的 sin/cos 使用弧度，所以要先转换。
    const double roll = degToRad(roll_deg);
    const double pitch = degToRad(pitch_deg);
    const double yaw = degToRad(yaw_deg);

    std::cout << "Roll  = " << roll_deg << " deg" << std::endl;
    std::cout << "Pitch = " << pitch_deg << " deg" << std::endl;
    std::cout << "Yaw   = " << yaw_deg << " deg" << std::endl;

    // -----------------------------
    // 3. 欧拉角转旋转矩阵
    // -----------------------------
    const Matrix3 rotation = eulerToRotationMatrix(roll, pitch, yaw);

    std::cout << std::endl;
    std::cout << "Rotation matrix R = Rz(yaw) * Ry(pitch) * Rx(roll):" << std::endl;
    printMatrix(rotation);

    // -----------------------------
    // 4. 定义机体坐标系中的推力方向
    // -----------------------------
    // 为了直观理解，这里假设机体向上的推力方向是 body_z_up。
    //
    // 注意：
    // PX4 常用 FRD 坐标，Z 轴向下。
    // 这里为了教学直观，用 {0, 0, 1} 表示“机体向上推力方向”。
    // 重点是理解姿态变化会改变推力方向。
    const Vector3 body_thrust_direction{0.0, 0.0, 1.0};

    // -----------------------------
    // 5. 计算世界坐标系中的推力方向
    // -----------------------------
    const Vector3 world_thrust_direction =
        multiply(rotation, body_thrust_direction);

    std::cout << std::endl;
    std::cout << "Body thrust direction:" << std::endl;
    printVector(body_thrust_direction);

    std::cout << "World thrust direction after attitude rotation:" << std::endl;
    printVector(world_thrust_direction);

    std::cout << std::endl;
    std::cout << "Interpretation:" << std::endl;
    std::cout << "- Roll changes left/right tilt." << std::endl;
    std::cout << "- Pitch changes forward/backward tilt." << std::endl;
    std::cout << "- Yaw changes heading direction." << std::endl;
    std::cout << "- When roll or pitch is not zero, thrust direction is no longer purely vertical." << std::endl;

    return 0;
}
