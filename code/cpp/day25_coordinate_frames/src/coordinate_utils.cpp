// 作用：
// 实现坐标系转换函数。
// 这些函数帮助理解 NED、ENU、FRD、FLU 之间的关系。

#include "coordinate_utils.hpp"

#include <cmath>
#include <iomanip>
#include <iostream>

double degToRad(double degree) {
    // 角度转弧度公式：
    // rad = degree * pi / 180
    return degree * M_PI / 180.0;
}

Vector3 nedToEnu(const Vector3& ned) {
    // NED:
    // x = north
    // y = east
    // z = down
    //
    // ENU:
    // x = east
    // y = north
    // z = up
    //
    // 所以：
    // x_enu = y_ned
    // y_enu = x_ned
    // z_enu = -z_ned
    return Vector3{
        ned[1],
        ned[0],
        -ned[2]
    };
}

Vector3 enuToNed(const Vector3& enu) {
    // ENU 转 NED：
    // x_ned = y_enu
    // y_ned = x_enu
    // z_ned = -z_enu
    return Vector3{
        enu[1],
        enu[0],
        -enu[2]
    };
}

Vector3 frdToFlu(const Vector3& frd) {
    // FRD:
    // x = forward
    // y = right
    // z = down
    //
    // FLU:
    // x = forward
    // y = left
    // z = up
    //
    // 前方不变，右变左取反，下变上取反。
    return Vector3{
        frd[0],
        -frd[1],
        -frd[2]
    };
}

Vector3 fluToFrd(const Vector3& flu) {
    // FLU 转 FRD：
    // x_frd = x_flu
    // y_frd = -y_flu
    // z_frd = -z_flu
    return Vector3{
        flu[0],
        -flu[1],
        -flu[2]
    };
}

Vector3 bodyFrdVelocityToNed(const Vector3& body_velocity_frd, double yaw_rad) {
    // 这个函数只考虑水平面 yaw 旋转，不考虑 roll 和 pitch。
    //
    // NED 世界系：
    // x 指北
    // y 指东
    //
    // FRD 机体系：
    // x 指机头前方
    // y 指机体右方
    //
    // 当 yaw = 0 时：
    // 机头朝北
    // body x 对应 NED x
    // body y 对应 NED y
    //
    // 当 yaw = 90° 时：
    // 机头朝东
    // body x 对应 NED y
    // body y 对应 NED -x

    const double c = std::cos(yaw_rad);
    const double s = std::sin(yaw_rad);

    const double vx_body = body_velocity_frd[0];
    const double vy_body = body_velocity_frd[1];
    const double vz_body = body_velocity_frd[2];

    // 水平速度旋转：
    // ned_x = cos(yaw) * body_x - sin(yaw) * body_y
    // ned_y = sin(yaw) * body_x + cos(yaw) * body_y
    //
    // z 方向同为 Down，所以直接保留。
    const double vx_ned = c * vx_body - s * vy_body;
    const double vy_ned = s * vx_body + c * vy_body;
    const double vz_ned = vz_body;

    return Vector3{
        vx_ned,
        vy_ned,
        vz_ned
    };
}

void printVector(const char* name, const Vector3& vector) {
    std::cout << std::fixed << std::setprecision(3);

    std::cout
        << name << " = [ "
        << vector[0] << ", "
        << vector[1] << ", "
        << vector[2] << " ]"
        << std::endl;
}
