#include "pid_controller.hpp"

#include <algorithm>
#include <stdexcept>

PIDController::PIDController(double kp, double ki, double kd)
    : kp_(kp),
      ki_(ki),
      kd_(kd),
      previous_error_(0.0),
      integral_(0.0),
      first_update_(true),
      min_output_(-1e9),
      max_output_(1e9),
      min_integral_(-1e9),
      max_integral_(1e9) {}

double PIDController::update(double setpoint, double measurement, double dt) {
    if (dt <= 0.0) {
        throw std::invalid_argument("dt must be positive");
    }

    const double error = setpoint - measurement;

    integral_ += error * dt;
    integral_ = clamp(integral_, min_integral_, max_integral_);

    double derivative = 0.0;

    if (!first_update_) {
        derivative = (error - previous_error_) / dt;
    }

    const double output =
        kp_ * error +
        ki_ * integral_ +
        kd_ * derivative;

    previous_error_ = error;
    first_update_ = false;

    return clamp(output, min_output_, max_output_);
}

void PIDController::reset() {
    previous_error_ = 0.0;
    integral_ = 0.0;
    first_update_ = true;
}

void PIDController::setGains(double kp, double ki, double kd) {
    kp_ = kp;
    ki_ = ki;
    kd_ = kd;
}

void PIDController::setOutputLimits(double min_output, double max_output) {
    if (min_output > max_output) {
        throw std::invalid_argument("min_output must be <= max_output");
    }

    min_output_ = min_output;
    max_output_ = max_output;
}

void PIDController::setIntegralLimits(double min_integral, double max_integral) {
    if (min_integral > max_integral) {
        throw std::invalid_argument("min_integral must be <= max_integral");
    }

    min_integral_ = min_integral;
    max_integral_ = max_integral;
}

double PIDController::getLastError() const {
    return previous_error_;
}

double PIDController::getIntegral() const {
    return integral_;
}

double PIDController::clamp(double value, double min_value, double max_value) const {
    return std::max(min_value, std::min(value, max_value));
}
