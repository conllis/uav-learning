// 作用：
// 演示 NED、ENU、FRD、FLU 坐标系之间的转换。
// 并演示在不同 yaw 角下，机体系“向前速度”在 NED 世界系中变成什么方向。

#include "coordinate_utils.hpp"

#include <iostream>

int main() {
    std::cout << "===== NED <-> ENU Example =====" << std::endl;

    // NED 向量：
    // x = north = 10 m
    // y = east  = 5 m
    // z = down  = -3 m
    //
    // z = -3 表示向上 3 m。
    const Vector3 position_ned{10.0, 5.0, -3.0};

    const Vector3 position_enu = nedToEnu(position_ned);
    const Vector3 position_ned_back = enuToNed(position_enu);

    printVector("position_ned", position_ned);
    printVector("position_enu", position_enu);
    printVector("position_ned_back", position_ned_back);

    std::cout << std::endl;
    std::cout << "===== FRD <-> FLU Example =====" << std::endl;

    // FRD 机体系向量：
    // x = forward = 2
    // y = right   = 1
    // z = down    = -0.5
    //
    // z = -0.5 表示机体系向上 0.5。
    const Vector3 body_frd{2.0, 1.0, -0.5};

    const Vector3 body_flu = frdToFlu(body_frd);
    const Vector3 body_frd_back = fluToFrd(body_flu);

    printVector("body_frd", body_frd);
    printVector("body_flu", body_flu);
    printVector("body_frd_back", body_frd_back);

    std::cout << std::endl;
    std::cout << "===== Body FRD Velocity -> NED Velocity =====" << std::endl;

    // 机体系速度：
    // x = 1 m/s，表示无人机向机头前方飞
    // y = 0
    // z = 0
    const Vector3 forward_velocity_body{1.0, 0.0, 0.0};

    // 情况 1：yaw = 0°，机头朝北。
    // 机体系向前 = NED 向北。
    const double yaw_0 = degToRad(0.0);
    const Vector3 velocity_ned_yaw_0 =
        bodyFrdVelocityToNed(forward_velocity_body, yaw_0);

    printVector("body_forward_velocity", forward_velocity_body);
    printVector("ned_velocity_yaw_0_deg", velocity_ned_yaw_0);

    // 情况 2：yaw = 90°，机头朝东。
    // 机体系向前 = NED 向东。
    const double yaw_90 = degToRad(90.0);
    const Vector3 velocity_ned_yaw_90 =
        bodyFrdVelocityToNed(forward_velocity_body, yaw_90);

    printVector("ned_velocity_yaw_90_deg", velocity_ned_yaw_90);

    // 情况 3：yaw = 180°，机头朝南。
    // 机体系向前 = NED 向南，也就是 NED x 为负。
    const double yaw_180 = degToRad(180.0);
    const Vector3 velocity_ned_yaw_180 =
        bodyFrdVelocityToNed(forward_velocity_body, yaw_180);

    printVector("ned_velocity_yaw_180_deg", velocity_ned_yaw_180);

    std::cout << std::endl;
    std::cout << "Key idea:" << std::endl;
    std::cout << "The same body-frame forward command means different world-frame directions when yaw changes." << std::endl;

    return 0;
}
