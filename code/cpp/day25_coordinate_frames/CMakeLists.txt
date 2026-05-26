# 作用：
# 构建 Day 25 坐标系转换练习程序。
# 程序包含：
# 1. main.cpp：实验入口
# 2. coordinate_utils.cpp：坐标转换工具函数

cmake_minimum_required(VERSION 3.16)

project(day25_coordinate_frames)

add_executable(day25_coordinate_frames
    src/main.cpp
    src/coordinate_utils.cpp
)

target_compile_features(day25_coordinate_frames PRIVATE cxx_std_17)

target_include_directories(day25_coordinate_frames PRIVATE
    include
)

target_compile_options(day25_coordinate_frames PRIVATE
    -Wall
    -Wextra
)
