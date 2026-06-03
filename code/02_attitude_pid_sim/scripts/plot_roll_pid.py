import csv
import matplotlib.pyplot as plt

time = []
target_roll = []
roll = []
roll_rate = []
torque = []

with open("data/roll_pid.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        time.append(float(row["time"]))
        target_roll.append(float(row["target_roll_deg"]))
        roll.append(float(row["roll_deg"]))
        roll_rate.append(float(row["roll_rate_deg_s"]))
        torque.append(float(row["torque_nm"]))

plt.figure()
plt.plot(time, target_roll, label="target roll")
plt.plot(time, roll, label="roll")
plt.xlabel("Time (s)")
plt.ylabel("Roll angle (deg)")
plt.title("Roll PID Response")
plt.legend()
plt.grid(True)
plt.savefig("plots/roll_pid_angle.png")

plt.figure()
plt.plot(time, roll_rate)
plt.xlabel("Time (s)")
plt.ylabel("Roll rate (deg/s)")
plt.title("Roll Rate")
plt.grid(True)
plt.savefig("plots/roll_pid_rate.png")

plt.figure()
plt.plot(time, torque)
plt.xlabel("Time (s)")
plt.ylabel("Torque (N*m)")
plt.title("Roll Torque Output")
plt.grid(True)
plt.savefig("plots/roll_pid_torque.png")

print("Plots saved to plots/")
