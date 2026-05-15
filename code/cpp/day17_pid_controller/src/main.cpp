#include "pid_controller.hpp"

#include <iostream>
#include <iomanip>

int main() {
    PIDController altitude_pid(0.8, 0.1, 0.2);

    altitude_pid.setOutputLimits(-3.0, 3.0);
    altitude_pid.setIntegralLimits(-10.0, 10.0);

    const double target_altitude = 10.0;
    double altitude = 0.0;

    const double dt = 0.1;
    const double simulation_time = 20.0;

    std::cout << std::fixed << std::setprecision(3);
    std::cout << "time,setpoint,altitude,control,error" << std::endl;

    for (double t = 0.0; t <= simulation_time; t += dt) {
        const double control = altitude_pid.update(target_altitude, altitude, dt);

        // 简化模型：把 PID 输出近似看作垂直速度
        altitude += control * dt;

        const double error = target_altitude - altitude;

        std::cout
            << t << ","
            << target_altitude << ","
            << altitude << ","
            << control << ","
            << error
            << std::endl;
    }

    return 0;
}
