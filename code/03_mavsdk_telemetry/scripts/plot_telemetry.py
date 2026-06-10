import os
import pandas as pd
import matplotlib.pyplot as plt


CSV_PATH = "data/px4_telemetry.csv"
PLOTS_DIR = "plots"


def ensure_output_dir() -> None:
    os.makedirs(PLOTS_DIR, exist_ok=True)


def load_data() -> pd.DataFrame:
    if not os.path.exists(CSV_PATH):
        raise FileNotFoundError(
            f"Cannot find {CSV_PATH}. Please run log_telemetry_csv.py first."
        )

    df = pd.read_csv(CSV_PATH)

    required_columns = [
        "time_s",
        "relative_altitude_m",
        "roll_deg",
        "pitch_deg",
        "yaw_deg",
        "flight_mode",
        "armed",
    ]

    for column in required_columns:
        if column not in df.columns:
            raise ValueError(f"Missing column in CSV: {column}")

    return df


def plot_relative_altitude(df: pd.DataFrame) -> None:
    plt.figure()
    plt.plot(df["time_s"], df["relative_altitude_m"])
    plt.xlabel("Time (s)")
    plt.ylabel("Relative altitude (m)")
    plt.title("PX4 Relative Altitude")
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, "relative_altitude.png"), dpi=150)
    plt.close()


def plot_attitude(df: pd.DataFrame) -> None:
    plt.figure()
    plt.plot(df["time_s"], df["roll_deg"], label="roll")
    plt.plot(df["time_s"], df["pitch_deg"], label="pitch")
    plt.plot(df["time_s"], df["yaw_deg"], label="yaw")
    plt.xlabel("Time (s)")
    plt.ylabel("Angle (deg)")
    plt.title("PX4 Attitude Euler Angles")
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, "attitude_euler.png"), dpi=150)
    plt.close()


def plot_flight_mode(df: pd.DataFrame) -> None:
    mode_codes = pd.Categorical(df["flight_mode"]).codes

    plt.figure()
    plt.plot(df["time_s"], mode_codes)
    plt.xlabel("Time (s)")
    plt.ylabel("Flight mode code")
    plt.title("PX4 Flight Mode")
    plt.grid(True)
    plt.savefig(os.path.join(PLOTS_DIR, "flight_mode.png"), dpi=150)
    plt.close()


def print_summary(df: pd.DataFrame) -> None:
    print("\n===== Telemetry Summary =====")
    print(f"Rows: {len(df)}")
    print(f"Duration: {df['time_s'].max():.2f} s")

    print("\nRelative altitude:")
    print(f"  min: {df['relative_altitude_m'].min():.3f} m")
    print(f"  max: {df['relative_altitude_m'].max():.3f} m")
    print(f"  last: {df['relative_altitude_m'].iloc[-1]:.3f} m")

    print("\nAttitude:")
    print(f"  roll min/max:  {df['roll_deg'].min():.3f} / {df['roll_deg'].max():.3f} deg")
    print(f"  pitch min/max: {df['pitch_deg'].min():.3f} / {df['pitch_deg'].max():.3f} deg")
    print(f"  yaw min/max:   {df['yaw_deg'].min():.3f} / {df['yaw_deg'].max():.3f} deg")

    print("\nFlight modes:")
    print(df["flight_mode"].value_counts())

    print("\nArmed states:")
    print(df["armed"].value_counts())


def main() -> None:
    ensure_output_dir()
    df = load_data()

    plot_relative_altitude(df)
    plot_attitude(df)
    plot_flight_mode(df)
    print_summary(df)

    print("\nPlots saved to:")
    print(f"  {PLOTS_DIR}/relative_altitude.png")
    print(f"  {PLOTS_DIR}/attitude_euler.png")
    print(f"  {PLOTS_DIR}/flight_mode.png")


if __name__ == "__main__":
    main()
