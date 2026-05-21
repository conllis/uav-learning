#include "altitude_simulator.hpp"
#include "pid_controller.hpp"

#include <fstream>
#include <iomanip>
#include <iostream>

int main() {
    const double mass = 1.5;
    const double gravity = 9.81;

    const double min_thrust = 0.0;
    const double max_thrust = 30.0;

    const double target_altitude = 10.0;

    const double dt = 0.01;
    const double simulation_time = 20.0;

    PIDController altitude_pid(2.0, 0.4, 1.2);
    altitude_pid.setOutputLimits(-5.0, 5.0);
    altitude_pid.setIntegralLimits(-8.0, 8.0);

    AltitudeSimulator simulator(mass, gravity, min_thrust, max_thrust);
    simulator.reset(0.0, 0.0);

    std::ofstream file("altitude_control_result.csv");

    if (!file.is_open()) {
        std::cerr << "Failed to open output file." << std::endl;
        return 1;
    }

    file << "time,setpoint,altitude,velocity,acceleration,thrust,error\n";

    std::cout << std::fixed << std::setprecision(3);
    std::cout << "Running altitude control simulation..." << std::endl;

    for (double t = 0.0; t <= simulation_time; t += dt) {
        const AltitudeState current_state = simulator.getState();

        const double acceleration_command =
            altitude_pid.update(target_altitude, current_state.altitude, dt);

        const AltitudeState new_state =
            simulator.update(acceleration_command, dt);

        const double error = target_altitude - new_state.altitude;

        file
            << t << ","
            << target_altitude << ","
            << new_state.altitude << ","
            << new_state.velocity << ","
            << new_state.acceleration << ","
            << new_state.thrust << ","
            << error
            << "\n";

        if (static_cast<int>(t * 100) % 100 == 0) {
            std::cout
                << "t = " << t
                << " s, altitude = " << new_state.altitude
                << " m, velocity = " << new_state.velocity
                << " m/s, error = " << error
                << " m"
                << std::endl;
        }
    }

    file.close();

    const AltitudeState final_state = simulator.getState();

    std::cout << "Simulation finished." << std::endl;
    std::cout << "Final altitude: " << final_state.altitude << " m" << std::endl;
    std::cout << "Result saved to altitude_control_result.csv" << std::endl;

    return 0;
}
