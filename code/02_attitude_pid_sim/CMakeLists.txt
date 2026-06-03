cmake_minimum_required(VERSION 3.16)

project(attitude_pid_sim)

add_executable(roll_pid_sim
    src/roll_pid_sim.cpp
    src/PIDController.cpp
)

target_include_directories(roll_pid_sim PRIVATE
    include
)

target_compile_features(roll_pid_sim PRIVATE cxx_std_17)

target_compile_options(roll_pid_sim PRIVATE
    -Wall
    -Wextra
)
