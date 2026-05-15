#include "altitude_analyzer.hpp"

#include <iostream>

AltitudeAnalyzer::AltitudeAnalyzer(const std::vector<SensorData>& data)
    : data_(data) {}

double AltitudeAnalyzer::meanAltitude() const {
    if (data_.empty()) {
        return 0.0;
    }

    double sum = 0.0;

    for (const auto& item : data_) {
        sum += item.altitude;
    }

    return sum / data_.size();
}

double AltitudeAnalyzer::maxAltitude() const {
    if (data_.empty()) {
        return 0.0;
    }

    double max_value = data_[0].altitude;

    for (const auto& item : data_) {
        if (item.altitude > max_value) {
            max_value = item.altitude;
        }
    }

    return max_value;
}

double AltitudeAnalyzer::finalAltitude() const {
    if (data_.empty()) {
        return 0.0;
    }

    return data_.back().altitude;
}

void AltitudeAnalyzer::printSummary() const {
    std::cout << "Altitude data count: " << data_.size() << std::endl;
    std::cout << "Mean altitude: " << meanAltitude() << " m" << std::endl;
    std::cout << "Max altitude: " << maxAltitude() << " m" << std::endl;
    std::cout << "Final altitude: " << finalAltitude() << " m" << std::endl;
}
