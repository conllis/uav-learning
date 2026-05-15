cmake_minimum_required(VERSION 3.16)

project(day17_pid_controller)

add_executable(day17_pid_controller
    src/main.cpp
    src/pid_controller.cpp
)

target_compile_features(day17_pid_controller PRIVATE cxx_std_17)

target_include_directories(day17_pid_controller PRIVATE
    include
)

target_compile_options(day17_pid_controller PRIVATE
    -Wall
    -Wextra
)
