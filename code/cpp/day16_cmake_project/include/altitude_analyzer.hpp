#pragma once

#include <vector>

struct SensorData {
    double time;
    double altitude;
    double velocity;
};

class AltitudeAnalyzer {
public:
    explicit AltitudeAnalyzer(const std::vector<SensorData>& data);

    double meanAltitude() const;
    double maxAltitude() const;
    double finalAltitude() const;

    void printSummary() const;

private:
    std::vector<SensorData> data_;
};
