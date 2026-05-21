#pragma once

struct AltitudeState {
    double altitude;
    double velocity;
    double acceleration;
    double thrust;
};

class AltitudeSimulator {
public:
    AltitudeSimulator(double mass, double gravity, double min_thrust, double max_thrust);

    void reset(double initial_altitude, double initial_velocity);

    AltitudeState update(double acceleration_command, double dt);

    AltitudeState getState() const;

private:
    double mass_;
    double gravity_;

    double min_thrust_;
    double max_thrust_;

    AltitudeState state_;

    double clamp(double value, double min_value, double max_value) const;
};
