cmake_minimum_required(VERSION 3.16)

project(day18_altitude_control_sim)

add_executable(day18_altitude_control_sim
    src/main.cpp
    src/pid_controller.cpp
    src/altitude_simulator.cpp
)

target_compile_features(day18_altitude_control_sim PRIVATE cxx_std_17)

target_include_directories(day18_altitude_control_sim PRIVATE
    include
)

target_compile_options(day18_altitude_control_sim PRIVATE
    -Wall
    -Wextra
)
