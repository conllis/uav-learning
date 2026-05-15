cmake_minimum_required(VERSION 3.16)

project(day16_cmake_project)

add_executable(day16_cmake_project
    src/main.cpp
    src/altitude_analyzer.cpp
)

target_compile_features(day16_cmake_project PRIVATE cxx_std_17)

target_include_directories(day16_cmake_project PRIVATE
    include
)

target_compile_options(day16_cmake_project PRIVATE
    -Wall
    -Wextra
)
