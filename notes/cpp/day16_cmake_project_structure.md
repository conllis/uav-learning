# Day 16 学习 CMake 工程结构

## 今日目标

学习如何组织一个标准 C++ + CMake 工程，为后续 PID 控制器和 PX4 源码阅读做准备。

---

## 1. 工程结构

```text
day16_cmake_project/
├── CMakeLists.txt
├── include/
│   └── altitude_analyzer.hpp
├── src/
│   ├── altitude_analyzer.cpp
│   └── main.cpp
└── build/
2. 各目录作用
include/

存放头文件，主要写类声明、结构体声明、函数声明。

src/

存放源文件，主要写函数和类的具体实现。

build/

存放编译产物，不应该提交到 Git。

3. hpp 和 cpp 的区别

.hpp 文件负责声明：

class AltitudeAnalyzer;

.cpp 文件负责实现：

double AltitudeAnalyzer::meanAltitude() const {
    // implementation
}
4. CMakeLists.txt 作用

CMakeLists.txt 描述项目如何编译。

本次项目中：

add_executable(day16_cmake_project
    src/main.cpp
    src/altitude_analyzer.cpp
)

表示用两个 .cpp 文件生成一个可执行程序。

5. include 路径
target_include_directories(day16_cmake_project PRIVATE
    include
)

表示编译器可以在 include/ 目录中查找头文件。

6. 编译命令
cmake -S . -B build
cmake --build build
./build/day16_cmake_project
7. 今日理解
.hpp：声明接口
.cpp：实现功能
main.cpp：使用功能
CMakeLists.txt：组织编译
build/：保存编译结果
今日总结

今天完成了一个标准 C++ 工程结构练习，把 Day 15 的高度分析代码拆分成头文件和源文件，并用 CMake 编译运行。

这个结构后续可以直接扩展为 PID 控制器项目。
