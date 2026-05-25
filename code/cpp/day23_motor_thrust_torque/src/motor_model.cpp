// 作用：
// 实现 MotorModel 类。
// 这里把电机和桨叶看成一个简化模型：
// 电机转得越快，桨叶产生的推力和反扭矩越大。
// 推力和反扭矩都近似与角速度平方成正比。

#include "motor_model.hpp"

#include <cmath>

MotorModel::MotorModel(double thrust_coefficient, double torque_coefficient)
    : thrust_coefficient_(thrust_coefficient),
      torque_coefficient_(torque_coefficient) {}

MotorOutput MotorModel::compute(double rpm, int direction) const {
    const double omega = rpmToOmega(rpm);

    // 推力公式：T = kf * omega^2
    const double thrust = thrust_coefficient_ * omega * omega;

    // 反扭矩公式：Q = km * omega^2
    // direction 用来表示旋向：
    // +1 表示一种旋向，-1 表示相反旋向。
    const double reaction_torque =
        static_cast<double>(direction) * torque_coefficient_ * omega * omega;

    return MotorOutput{
        rpm,
        omega,
        thrust,
        reaction_torque
    };
}

double MotorModel::rpmToOmega(double rpm) const {
    // RPM 转 rad/s：
    // omega = rpm * 2*pi / 60
    return rpm * 2.0 * M_PI / 60.0;
}
