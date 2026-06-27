import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main():
    if len(sys.argv) >= 2:
        csv_path = Path(sys.argv[1])
    else:
        csv_path = Path.home() / "uav-learning" / "data" / "month3" / "offboard_square.csv"

    output_dir = Path.home() / "uav-learning" / "plots" / "month3"
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(csv_path)

    df["time_sec"] = pd.to_numeric(df["time_sec"], errors="coerce")
    df["relative_altitude_m"] = pd.to_numeric(df["relative_altitude_m"], errors="coerce")
    df["roll_deg"] = pd.to_numeric(df["roll_deg"], errors="coerce")
    df["pitch_deg"] = pd.to_numeric(df["pitch_deg"], errors="coerce")
    df["yaw_deg"] = pd.to_numeric(df["yaw_deg"], errors="coerce")
    df["north_m"] = pd.to_numeric(df["north_m"], errors="coerce")
    df["east_m"] = pd.to_numeric(df["east_m"], errors="coerce")

    # 高度曲线
    plt.figure()
    plt.plot(df["time_sec"], df["relative_altitude_m"])
    plt.xlabel("Time (s)")
    plt.ylabel("Relative altitude (m)")
    plt.title("Offboard Relative Altitude")
    plt.grid(True)
    plt.savefig(output_dir / "offboard_altitude.png", dpi=200)
    plt.close()

    # 姿态曲线
    plt.figure()
    plt.plot(df["time_sec"], df["roll_deg"], label="roll")
    plt.plot(df["time_sec"], df["pitch_deg"], label="pitch")
    plt.plot(df["time_sec"], df["yaw_deg"], label="yaw")
    plt.xlabel("Time (s)")
    plt.ylabel("Attitude (deg)")
    plt.title("Offboard Attitude")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_dir / "offboard_attitude.png", dpi=200)
    plt.close()

    # mission phase 曲线
    phases = df["mission_phase"].astype("category")
    df["phase_code"] = phases.cat.codes

    plt.figure()
    plt.plot(df["time_sec"], df["phase_code"])
    plt.xlabel("Time (s)")
    plt.ylabel("Mission phase code")
    plt.title("Offboard Mission Phase")
    plt.grid(True)
    plt.savefig(output_dir / "offboard_phase.png", dpi=200)
    plt.close()

    # x/y 轨迹
    if "north_m" in df.columns and "east_m" in df.columns:
        plt.figure()
        plt.plot(df["east_m"], df["north_m"])
        plt.xlabel("East (m)")
        plt.ylabel("North (m)")
        plt.title("Offboard XY Trajectory")
        plt.grid(True)
        plt.axis("equal")
        plt.savefig(output_dir / "offboard_xy_trajectory.png", dpi=200)
        plt.close()

    print(f"Plots saved to: {output_dir}")


if __name__ == "__main__":
    main()
