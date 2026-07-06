import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def run_complementary_filter_demo():
    # -----------------------------
    # 1. 基本仿真参数
    # -----------------------------
    dt = 0.01
    duration_sec = 20.0
    alpha = 0.98

    time_array = np.arange(0.0, duration_sec, dt)

    # -----------------------------
    # 2. 构造“真实角度”
    # -----------------------------
    # 模拟无人机 roll 角变化，单位：deg
    true_angle = 15.0 * np.sin(0.8 * time_array) + 5.0 * np.sin(2.0 * time_array)

    # 真实角速度，单位：deg/s
    true_gyro_rate = np.gradient(true_angle, dt)

    # -----------------------------
    # 3. 模拟陀螺仪测量
    # -----------------------------
    rng = np.random.default_rng(seed=42)

    gyro_bias = 0.6
    gyro_noise = rng.normal(0.0, 0.8, size=len(time_array))

    measured_gyro_rate = true_gyro_rate + gyro_bias + gyro_noise

    # -----------------------------
    # 4. 模拟加速度计角度估计
    # -----------------------------
    accel_noise = rng.normal(0.0, 2.5, size=len(time_array))

    # 模拟 8s 到 12s 之间机体运动或振动导致加速度计受干扰
    accel_disturbance = np.zeros_like(time_array)
    disturbance_mask = (time_array >= 8.0) & (time_array <= 12.0)
    accel_disturbance[disturbance_mask] = 6.0 * np.sin(25.0 * time_array[disturbance_mask])

    accel_angle = true_angle + accel_noise + accel_disturbance

    # -----------------------------
    # 5. 仅使用陀螺仪积分
    # -----------------------------
    gyro_angle = np.zeros_like(time_array)
    gyro_angle[0] = true_angle[0]

    for i in range(1, len(time_array)):
        gyro_angle[i] = gyro_angle[i - 1] + measured_gyro_rate[i] * dt

    # -----------------------------
    # 6. 互补滤波
    # -----------------------------
    complementary_angle = np.zeros_like(time_array)
    complementary_angle[0] = accel_angle[0]

    for i in range(1, len(time_array)):
        gyro_prediction = complementary_angle[i - 1] + measured_gyro_rate[i] * dt

        complementary_angle[i] = (
            alpha * gyro_prediction
            + (1.0 - alpha) * accel_angle[i]
        )

    # -----------------------------
    # 7. 保存 CSV
    # -----------------------------
    data_path = Path.home() / "uav-learning" / "data" / "month3" / "complementary_filter_data.csv"
    data_path.parent.mkdir(parents=True, exist_ok=True)

    with open(data_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow([
            "time_sec",
            "true_angle_deg",
            "accel_angle_deg",
            "gyro_angle_deg",
            "complementary_angle_deg",
            "measured_gyro_rate_deg_s",
        ])

        for i in range(len(time_array)):
            writer.writerow([
                f"{time_array[i]:.3f}",
                f"{true_angle[i]:.6f}",
                f"{accel_angle[i]:.6f}",
                f"{gyro_angle[i]:.6f}",
                f"{complementary_angle[i]:.6f}",
                f"{measured_gyro_rate[i]:.6f}",
            ])

    # -----------------------------
    # 8. 画图
    # -----------------------------
    plot_path = Path.home() / "uav-learning" / "plots" / "month3" / "complementary_filter.png"
    plot_path.parent.mkdir(parents=True, exist_ok=True)

    plt.figure(figsize=(12, 6))
    plt.plot(time_array, true_angle, label="True angle")
    plt.plot(time_array, accel_angle, label="Accel angle", alpha=0.5)
    plt.plot(time_array, gyro_angle, label="Gyro integration")
    plt.plot(time_array, complementary_angle, label=f"Complementary filter alpha={alpha}")

    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.title("Complementary Filter Demo")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(plot_path, dpi=200)
    plt.close()

    # -----------------------------
    # 9. 计算误差
    # -----------------------------
    accel_rmse = compute_rmse(accel_angle, true_angle)
    gyro_rmse = compute_rmse(gyro_angle, true_angle)
    complementary_rmse = compute_rmse(complementary_angle, true_angle)

    print("Complementary filter demo finished.")
    print(f"CSV saved to: {data_path}")
    print(f"Plot saved to: {plot_path}")
    print()
    print("RMSE:")
    print(f"  Accel angle:          {accel_rmse:.3f} deg")
    print(f"  Gyro integration:     {gyro_rmse:.3f} deg")
    print(f"  Complementary filter: {complementary_rmse:.3f} deg")


def compute_rmse(estimate, truth):
    error = estimate - truth
    return math.sqrt(float(np.mean(error ** 2)))


if __name__ == "__main__":
    run_complementary_filter_demo()
