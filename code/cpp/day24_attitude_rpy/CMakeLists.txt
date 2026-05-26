# 作用：
# 构建 Day 24 姿态角 roll / pitch / yaw 演示程序。
# 程序包含：
# 1. main.cpp：实验入口
# 2. attitude_utils.cpp：姿态角计算工具

cmake_minimum_required(VERSION 3.16)

project(day24_attitude_rpy)

add_executable(day24_attitude_rpy
    src/main.cpp
    src/attitude_utils.cpp
)

target_compile_features(day24_attitude_rpy PRIVATE cxx_std_17)

target_include_directories(day24_attitude_rpy PRIVATE
    include
)

target_compile_options(day24_attitude_rpy PRIVATE
    -Wall
    -Wextra
)
