# 作用：
# 构建 Day 23 电机-桨叶-推力-力矩关系演示程序。
# 程序由 main.cpp 和 motor_model.cpp 组成。

cmake_minimum_required(VERSION 3.16)

project(day23_motor_thrust_torque)

add_executable(day23_motor_thrust_torque
    src/main.cpp
    src/motor_model.cpp
)

target_compile_features(day23_motor_thrust_torque PRIVATE cxx_std_17)

target_include_directories(day23_motor_thrust_torque PRIVATE
    include
)

target_compile_options(day23_motor_thrust_torque PRIVATE
    -Wall
    -Wextra
)
