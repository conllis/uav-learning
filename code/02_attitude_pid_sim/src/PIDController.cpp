#include "PIDController.hpp"

PIDController::PIDController(double kp, double ki, double kd,
                             double output_min, double output_max)
    : kp_(kp),
      ki_(ki),
      kd_(kd),
      integral_(0.0),
      previous_error_(0.0),
      output_min_(output_min),
      output_max_(output_max),
      first_update_(true) {}

double PIDController::update(double target, double current, double dt) {
    const double error = target - current;

    integral_ += error * dt;

    double derivative = 0.0;
    if (!first_update_) {
        derivative = (error - previous_error_) / dt;
    }

    double output = kp_ * error + ki_ * integral_ + kd_ * derivative;

    if (output > output_max_) {
        output = output_max_;
    }

    if (output < output_min_) {
        output = output_min_;
    }

    previous_error_ = error;
    first_update_ = false;

    return output;
}

void PIDController::reset() {
    integral_ = 0.0;
    previous_error_ = 0.0;
    first_update_ = true;
}
