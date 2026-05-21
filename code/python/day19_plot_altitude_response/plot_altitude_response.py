# 作用：
# 读取 Day 18 高度控制仿真生成的 CSV 文件，
# 画出高度响应曲线、误差曲线、速度曲线和推力曲线。
#
# 输入文件：
# ~/uav-learning/code/cpp/day18_altitude_control_sim/altitude_control_result.csv
#
# 输出图片：
# ~/uav-learning/figures/day19/altitude_response.png
# ~/uav-learning/figures/day19/altitude_error.png
# ~/uav-learning/figures/day19/velocity_response.png
# ~/uav-learning/figures/day19/thrust_response.png

from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


def main():
    # 获取当前脚本所在位置
    script_dir = Path(__file__).resolve().parent

    # 项目根目录：~/uav-learning
    project_root = script_dir.parents[2]

    # Day 18 生成的 CSV 文件路径
    csv_path = project_root / "code" / "cpp" / "day18_altitude_control_sim" / "altitude_control_result.csv"

    # 图片输出目录
    figure_dir = project_root / "figures" / "day19"
    figure_dir.mkdir(parents=True, exist_ok=True)

    # 检查 CSV 是否存在
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    # 读取 CSV 数据
    data = pd.read_csv(csv_path)

    # 打印前几行，方便确认数据读取成功
    print("Loaded CSV:")
    print(data.head())

    # 提取数据列
    time = data["time"]
    setpoint = data["setpoint"]
    altitude = data["altitude"]
    velocity = data["velocity"]
    thrust = data["thrust"]
    error = data["error"]

    # 1. 高度响应曲线
    plt.figure()
    plt.plot(time, setpoint, label="Target altitude")
    plt.plot(time, altitude, label="Actual altitude")
    plt.xlabel("Time (s)")
    plt.ylabel("Altitude (m)")
    plt.title("Altitude Response")
    plt.grid(True)
    plt.legend()
    plt.savefig(figure_dir / "altitude_response.png", dpi=150, bbox_inches="tight")
    plt.close()

    # 2. 高度误差曲线
    plt.figure()
    plt.plot(time, error, label="Altitude error")
    plt.xlabel("Time (s)")
    plt.ylabel("Error (m)")
    plt.title("Altitude Error")
    plt.grid(True)
    plt.legend()
    plt.savefig(figure_dir / "altitude_error.png", dpi=150, bbox_inches="tight")
    plt.close()

    # 3. 速度曲线
    plt.figure()
    plt.plot(time, velocity, label="Vertical velocity")
    plt.xlabel("Time (s)")
    plt.ylabel("Velocity (m/s)")
    plt.title("Vertical Velocity Response")
    plt.grid(True)
    plt.legend()
    plt.savefig(figure_dir / "velocity_response.png", dpi=150, bbox_inches="tight")
    plt.close()

    # 4. 推力曲线
    plt.figure()
    plt.plot(time, thrust, label="Thrust")
    plt.xlabel("Time (s)")
    plt.ylabel("Thrust (N)")
    plt.title("Thrust Response")
    plt.grid(True)
    plt.legend()
    plt.savefig(figure_dir / "thrust_response.png", dpi=150, bbox_inches="tight")
    plt.close()

    print("Figures saved to:")
    print(figure_dir)


if __name__ == "__main__":
    main()
