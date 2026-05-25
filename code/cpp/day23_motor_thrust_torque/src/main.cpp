// 作用：
// 使用 MotorModel 计算四个电机在不同 RPM 下的推力和反扭矩。
// 通过这个程序理解：
// 1. 电机转速如何变成推力
// 2. 电机转速如何变成反扭矩
// 3. 四个电机如何合成总推力和 yaw 力矩

#include "motor_model.hpp"

#include <iomanip>
#include <iostream>
#include <vector>

int main() {
    // 简化模型参数。
    // 注意：这里的 kf 和 km 是教学用示例值，不代表真实电机参数。
    const double kf = 1.2e-5;
    const double km = 2.0e-7;

    MotorModel motor(kf, km);

    // 四个电机的 RPM。
    // 可以修改这些值观察总推力和 yaw 力矩变化。
    std::vector<double> rpms = {
        6000.0,
        6000.0,
        6000.0,
        6000.0
    };

    // 电机旋向。
    // +1 和 -1 表示两组相反旋向。
    // 注意：实际机型中旋向和电机编号要以飞控配置为准。
    std::vector<int> directions = {
        +1,
        -1,
        +1,
        -1
    };

    double total_thrust = 0.0;
    double total_yaw_torque = 0.0;

    std::cout << std::fixed << std::setprecision(4);

    std::cout << "motor,rpm,omega_rad_s,thrust_N,reaction_torque_Nm"
              << std::endl;

    for (std::size_t i = 0; i < rpms.size(); ++i) {
        const MotorOutput output = motor.compute(rpms[i], directions[i]);

        total_thrust += output.thrust;
        total_yaw_torque += output.reaction_torque;

        std::cout
            << "M" << (i + 1) << ","
            << output.rpm << ","
            << output.omega << ","
            << output.thrust << ","
            << output.reaction_torque
            << std::endl;
    }

    std::cout << std::endl;
    std::cout << "Total thrust: " << total_thrust << " N" << std::endl;
    std::cout << "Total yaw torque: " << total_yaw_torque << " N*m" << std::endl;

    return 0;
}
