#include "altitude_analyzer.hpp"

#include <vector>

int main() {
    std::vector<SensorData> flight_data = {
        {0.0, 0.0, 0.0},
        {1.0, 1.2, 1.2},
        {2.0, 2.5, 1.3},
        {3.0, 3.1, 0.6},
        {4.0, 3.0, -0.1},
    };

    AltitudeAnalyzer analyzer(flight_data);
    analyzer.printSummary();

    return 0;
}
