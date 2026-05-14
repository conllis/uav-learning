#include <iostream>
#include <vector>
#include <string>
#include <numeric>

struct SensorData {
    double time;
    double altitude;
    double velocity;
};

class AltitudeAnalyzer {
public:
    explicit AltitudeAnalyzer(const std::vector<SensorData>& data)
        : data_(data) {}

    double meanAltitude() const {
        if (data_.empty()) {
            return 0.0;
        }

        double sum = 0.0;
        for (const auto& item : data_) {
            sum += item.altitude;
        }

        return sum / data_.size();
    }

	double finalAltitude() const {
	    if (data_.empty()) {
	        return 0.0;
	    }

	    return data_.back().altitude;
	}

    double maxAltitude() const {
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

    void printSummary() const {
        std::cout << "Altitude data count: " << data_.size() << std::endl;
        std::cout << "Mean altitude: " << meanAltitude() << " m" << std::endl;
        std::cout << "Max altitude: " << maxAltitude() << " m" << std::endl;
	std::cout << "Final altitude:" << finalAltitude() << " m" << std::endl;
    }

private:
    std::vector<SensorData> data_;
};

int main() {
    std::vector<SensorData> flight_data = {
        {0.0, 0.0, 0.0},
        {1.0, 1.2, 1.2},
        {2.0, 2.5, 1.3},
        {3.0, 3.1, 0.6},
        {4.0, 3.0, -0.1}
    };

    AltitudeAnalyzer analyzer(flight_data);
    analyzer.printSummary();

    return 0;
}
