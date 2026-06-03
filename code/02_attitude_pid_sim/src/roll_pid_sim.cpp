#include "PIDController.hpp"

#include <cmath>
#include <fstream>
#include <iostream>

double degToRad(double degree) {
    return degree * M_PI / 180.0;
}

double radToDeg(double radian) {
    return radian * 180.0 / M_PI;
}

int main() {
    // -----------------------------
    // 1. 仿真参数
    // -----------------------------
    const double dt = 0.01;          // 时间步长，单位 s
    const double total_time = 5.0;   // 总仿真时间，单位 s

    // -----------------------------
    // 2. roll 目标角
    // -----------------------------
    const double target_roll_deg = 10.0;
    const double target_roll = degToRad(target_roll_deg);

    // -----------------------------
    // 3. 简化机体参数
    // -----------------------------
    // Ixx 是绕 roll 轴的转动惯量。
    // 这里是教学用假设值，不代表真实无人机。
    const double Ixx = 0.02;

    // -----------------------------
    // 4. 初始状态
    // -----------------------------
    double roll = degToRad(0.0);    // 当前 roll 角，单位 rad
    double roll_rate = 0.0;         // 当前 roll 角速度，单位 rad/s

    // -----------------------------
    // 5. PID 参数
    // -----------------------------
    // 输出限制表示最大/最小 roll 力矩。
    PIDController roll_pid(
        0.08,   // kp
        0.00,   // ki
        0.015,  // kd
        -0.2,   // output_min, Nm
        0.2     // output_max, Nm
    );

    // -----------------------------
    // 6. 打开 CSV 文件
    // -----------------------------
    std::ofstream file("data/roll_pid.csv");
    if (!file.is_open()) {
        std::cerr << "Failed to open data/roll_pid.csv" << std::endl;
        return 1;
    }

    file << "time,target_roll_deg,roll_deg,roll_rate_deg_s,torque_nm\n";

    // -----------------------------
    // 7. 仿真循环
    // -----------------------------
    for (double t = 0.0; t <= total_time; t += dt) {
        // PID 根据目标 roll 和当前 roll 计算 roll 力矩
        const double torque = roll_pid.update(target_roll, roll, dt);

        // 力矩产生角加速度
        const double roll_acceleration = torque / Ixx;

        // 角加速度积分得到角速度
        roll_rate += roll_acceleration * dt;

        // 角速度积分得到 roll 角
        roll += roll_rate * dt;

        file << t << ","
             << target_roll_deg << ","
             << radToDeg(roll) << ","
             << radToDeg(roll_rate) << ","
             << torque << "\n";
    }

    file.close();

    std::cout << "Roll PID simulation finished." << std::endl;
    std::cout << "Target roll: " << target_roll_deg << " deg" << std::endl;
    std::cout << "Result saved to data/roll_pid.csv" << std::endl;

    return 0;
}
