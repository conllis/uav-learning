#pragma once

class PIDController {
public:
    PIDController(double kp, double ki, double kd);

    double update(double setpoint, double measurement, double dt);

    void reset();

    void setGains(double kp, double ki, double kd);
    void setOutputLimits(double min_output, double max_output);
    void setIntegralLimits(double min_integral, double max_integral);

    double getLastError() const;
    double getIntegral() const;

private:
    double kp_;
    double ki_;
    double kd_;

    double previous_error_;
    double integral_;
    bool first_update_;

    double min_output_;
    double max_output_;

    double min_integral_;
    double max_integral_;

    double clamp(double value, double min_value, double max_value) const;
};
