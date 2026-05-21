#include "altitude_simulator.hpp"

#include <algorithm>
#include <stdexcept>

AltitudeSimulator::AltitudeSimulator(
    double mass,
    double gravity,
    double min_thrust,
    double max_thrust)
    : mass_(mass),
      gravity_(gravity),
      min_thrust_(min_thrust),
      max_thrust_(max_thrust),
      state_{0.0, 0.0, 0.0, 0.0} {
    if (mass_ <= 0.0) {
        throw std::invalid_argument("mass must be positive");
    }

    if (gravity_ <= 0.0) {
        throw std::invalid_argument("gravity must be positive");
    }

    if (min_thrust_ > max_thrust_) {
        throw std::invalid_argument("min_thrust must be <= max_thrust");
    }
}

void AltitudeSimulator::reset(double initial_altitude, double initial_velocity) {
    state_.altitude = initial_altitude;
    state_.velocity = initial_velocity;
    state_.acceleration = 0.0;
    state_.thrust = mass_ * gravity_;
}

AltitudeState AltitudeSimulator::update(double acceleration_command, double dt) {
    if (dt <= 0.0) {
        throw std::invalid_argument("dt must be positive");
    }

    // 推力 = 重力补偿 + 期望加速度对应的力
    double thrust = mass_ * (gravity_ + acceleration_command);
    thrust = clamp(thrust, min_thrust_, max_thrust_);

    const double acceleration = (thrust - mass_ * gravity_) / mass_;

    state_.velocity += acceleration * dt;
    state_.altitude += state_.velocity * dt;

    // 简单地面约束：高度不能小于 0
    if (state_.altitude < 0.0) {
        state_.altitude = 0.0;

        if (state_.velocity < 0.0) {
            state_.velocity = 0.0;
        }
    }

    state_.acceleration = acceleration;
    state_.thrust = thrust;

    return state_;
}

AltitudeState AltitudeSimulator::getState() const {
    return state_;
}

double AltitudeSimulator::clamp(double value, double min_value, double max_value) const {
    return std::max(min_value, std::min(value, max_value));
}
