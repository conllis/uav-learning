# Day 15 复习 C++ 基础语法

## 今日目标

复习 C++ 基础语法，为后续 PID 控制器、飞控仿真和 PX4 源码阅读做准备。

---

## 1. 今日复习内容

- 变量与类型
- if / else
- for / while
- 函数
- struct
- class
- vector
- const
- 引用
- CMake 编译

---

## 2. 今日练习项目

项目路径：

```bash
code/cpp/day15_cpp_basic

编译运行：

cd ~/uav-learning/code/cpp/day15_cpp_basic
mkdir -p build
cd build
cmake ..
make
./day15_cpp_basic
3. struct 的作用

struct 用于组织一组相关数据。

示例：

struct SensorData {
    double time;
    double altitude;
    double velocity;
};

在无人机项目中，可以用 struct 表示 IMU、GPS、高度、姿态等数据。

4. vector 的作用

std::vector 是动态数组，可以保存一组数据。

示例：

std::vector<SensorData> flight_data;

可以用于保存飞行轨迹、传感器序列、日志数据。

5. class 的作用

class 用于封装数据和方法。

本次练习中：

class AltitudeAnalyzer

用于分析高度数据。

后续可以写：

class PIDController

用于实现 PID 控制器。

6. const 引用
const std::vector<SensorData>& data

含义：

&：引用，避免复制大对象
const：不允许修改传入数据

工程中传递较大的对象时，通常使用 const 引用。

7. 今日总结

今天完成了一个简单的 C++ 飞行高度数据分析程序，复习了 struct、class、vector、函数、const 引用和 CMake 编译流程。

这为后续实现 PID 控制器和飞行数据分析打基础。
