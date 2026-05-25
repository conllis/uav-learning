// 作用：
// 定义一个简化电机模型 MotorModel。
// 该模型根据电机 RPM 计算：
// 1. 角速度 omega
// 2. 螺旋桨推力 thrust
// 3. 螺旋桨反扭矩 reaction_torque
//
// 使用的简化公式：
// omega = rpm * 2 * pi / 60
// thrust = kf * omega^2
// reaction_torque = direction * km * omega^2

#pragma once

struct MotorOutput {
    double rpm;
    double omega;
    double thrust;
    double reaction_torque;
};

class MotorModel {
public:
    MotorModel(double thrust_coefficient, double torque_coefficient);

    MotorOutput compute(double rpm, int direction) const;

private:
    double thrust_coefficient_;
    double torque_coefficient_;

    double rpmToOmega(double rpm) const;
};
