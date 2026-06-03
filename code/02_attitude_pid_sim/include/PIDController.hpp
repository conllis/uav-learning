#pragma once

class PIDController {
public:
    PIDController(double kp, double ki, double kd,
                  double output_min, double output_max);

    double update(double target, double current, double dt);
    void reset();

private:
    double kp_;
    double ki_;
    double kd_;

    double integral_;
    double previous_error_;

    double output_min_;
    double output_max_;

    bool first_update_;
};
