import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def main():
    t = np.linspace(0, 10, 200)
    y = np.sin(t)

    df = pd.DataFrame({
        "time": t,
        "value": y,
    })

    print("Python environment works.")
    print(df.head())

    plt.figure()
    plt.plot(df["time"], df["value"])
    plt.xlabel("time")
    plt.ylabel("sin(time)")
    plt.title("Day 03 Python Test")
    plt.grid(True)
    plt.savefig("day03_python_test.png", dpi=150)

    print("Saved figure: day03_python_test.png")


if __name__ == "__main__":
    main()
