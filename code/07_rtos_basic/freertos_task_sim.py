import asyncio
import csv
import math
import random
import time
from dataclasses import dataclass
from pathlib import Path


SIM_DURATION_SEC = 8.0

IMU_PERIOD_SEC = 0.005        # 200Hz
ATTITUDE_PERIOD_SEC = 0.005   # 200Hz
CONTROL_PERIOD_SEC = 0.01     # 100Hz
SAFETY_PERIOD_SEC = 0.05      # 20Hz
TELEMETRY_PERIOD_SEC = 0.1    # 10Hz
HEARTBEAT_PERIOD_SEC = 1.0    # 1Hz


@dataclass
class ImuData:
    ax: float
    ay: float
    az: float
    gx: float
    gy: float
    gz: float
    timestamp: float


@dataclass
class AttitudeData:
    roll: float
    pitch: float
    yaw: float
    timestamp: float


@dataclass
class MotorOutput:
    motor1: float
    motor2: float
    motor3: float
    motor4: float
    timestamp: float


class SystemState:
    def __init__(self):
        self.start_time = time.monotonic()

        self.latest_imu = None
        self.latest_attitude = None
        self.latest_motor = None

        self.imu_count = 0
        self.attitude_count = 0
        self.control_count = 0
        self.telemetry_count = 0
        self.safety_count = 0
        self.heartbeat_count = 0

        self.safety_ok = True
        self.last_imu_time = None
        self.last_control_time = None

        self.log_rows = []

    def now(self):
        return time.monotonic() - self.start_time

    def should_run(self):
        return self.now() < SIM_DURATION_SEC

    def log(self, task_name, message):
        self.log_rows.append([
            f"{self.now():.4f}",
            task_name,
            message,
            self.imu_count,
            self.attitude_count,
            self.control_count,
            self.telemetry_count,
            self.safety_count,
            self.heartbeat_count,
            self.safety_ok,
        ])


def overwrite_queue(queue, item):
    if queue.full():
        try:
            queue.get_nowait()
        except asyncio.QueueEmpty:
            pass

    queue.put_nowait(item)


async def wait_next_period(next_time, period_sec):
    next_time += period_sec
    sleep_time = next_time - time.monotonic()

    if sleep_time > 0:
        await asyncio.sleep(sleep_time)

    return next_time


async def imu_task(state, imu_queue):
    next_time = time.monotonic()

    while state.should_run():
        t = state.now()

        true_roll = 10.0 * math.sin(2.0 * math.pi * 0.25 * t)
        true_pitch = 5.0 * math.sin(2.0 * math.pi * 0.2 * t)

        roll_rad = math.radians(true_roll)
        pitch_rad = math.radians(true_pitch)

        ax = -math.sin(pitch_rad) + random.gauss(0.0, 0.02)
        ay = math.sin(roll_rad) * math.cos(pitch_rad) + random.gauss(0.0, 0.02)
        az = math.cos(roll_rad) * math.cos(pitch_rad) + random.gauss(0.0, 0.02)

        gx = 15.0 * math.cos(2.0 * math.pi * 0.25 * t) + random.gauss(0.0, 0.5)
        gy = 6.0 * math.cos(2.0 * math.pi * 0.2 * t) + random.gauss(0.0, 0.5)
        gz = 2.0 + random.gauss(0.0, 0.2)

        imu = ImuData(
            ax=ax,
            ay=ay,
            az=az,
            gx=gx,
            gy=gy,
            gz=gz,
            timestamp=t,
        )

        state.latest_imu = imu
        state.last_imu_time = t
        state.imu_count += 1

        overwrite_queue(imu_queue, imu)

        if state.imu_count % 100 == 0:
            state.log("imu_task", "read imu data")

        next_time = await wait_next_period(next_time, IMU_PERIOD_SEC)


async def attitude_task(state, imu_queue, attitude_queue):
    next_time = time.monotonic()

    roll = 0.0
    pitch = 0.0
    yaw = 0.0
    alpha = 0.98
    last_timestamp = None

    while state.should_run():
        imu = None

        try:
            imu = imu_queue.get_nowait()
        except asyncio.QueueEmpty:
            imu = state.latest_imu

        if imu is not None:
            if last_timestamp is None:
                dt = ATTITUDE_PERIOD_SEC
            else:
                dt = imu.timestamp - last_timestamp

            if dt <= 0:
                dt = ATTITUDE_PERIOD_SEC

            last_timestamp = imu.timestamp

            accel_roll = math.degrees(math.atan2(imu.ay, imu.az))
            accel_pitch = math.degrees(
                math.atan2(-imu.ax, math.sqrt(imu.ay * imu.ay + imu.az * imu.az))
            )

            roll = alpha * (roll + imu.gx * dt) + (1.0 - alpha) * accel_roll
            pitch = alpha * (pitch + imu.gy * dt) + (1.0 - alpha) * accel_pitch
            yaw = yaw + imu.gz * dt

            attitude = AttitudeData(
                roll=roll,
                pitch=pitch,
                yaw=yaw,
                timestamp=state.now(),
            )

            state.latest_attitude = attitude
            state.attitude_count += 1

            overwrite_queue(attitude_queue, attitude)

            if state.attitude_count % 100 == 0:
                state.log("attitude_task", "estimate attitude")

        next_time = await wait_next_period(next_time, ATTITUDE_PERIOD_SEC)


async def control_task(state, attitude_queue):
    next_time = time.monotonic()

    target_roll = 0.0
    target_pitch = 0.0
    base_throttle = 0.5
    kp = 0.01

    while state.should_run():
        attitude = None

        try:
            attitude = attitude_queue.get_nowait()
        except asyncio.QueueEmpty:
            attitude = state.latest_attitude

        if attitude is not None:
            roll_error = target_roll - attitude.roll
            pitch_error = target_pitch - attitude.pitch

            roll_cmd = kp * roll_error
            pitch_cmd = kp * pitch_error

            motor = MotorOutput(
                motor1=base_throttle + roll_cmd + pitch_cmd,
                motor2=base_throttle - roll_cmd + pitch_cmd,
                motor3=base_throttle - roll_cmd - pitch_cmd,
                motor4=base_throttle + roll_cmd - pitch_cmd,
                timestamp=state.now(),
            )

            state.latest_motor = motor
            state.last_control_time = state.now()
            state.control_count += 1

            if state.control_count % 50 == 0:
                state.log("control_task", "update motor output")

        next_time = await wait_next_period(next_time, CONTROL_PERIOD_SEC)


async def telemetry_task(state):
    next_time = time.monotonic()

    while state.should_run():
        attitude = state.latest_attitude
        motor = state.latest_motor

        state.telemetry_count += 1

        if attitude is not None and motor is not None:
            print(
                f"[TELEMETRY] t={state.now():.2f}s | "
                f"roll={attitude.roll:.2f}, pitch={attitude.pitch:.2f}, yaw={attitude.yaw:.2f} | "
                f"m1={motor.motor1:.2f}, m2={motor.motor2:.2f}, "
                f"m3={motor.motor3:.2f}, m4={motor.motor4:.2f} | "
                f"safety_ok={state.safety_ok}"
            )

        state.log("telemetry_task", "send telemetry")

        next_time = await wait_next_period(next_time, TELEMETRY_PERIOD_SEC)


async def safety_task(state):
    next_time = time.monotonic()

    while state.should_run():
        now = state.now()

        imu_timeout = (
            state.last_imu_time is None
            or now - state.last_imu_time > 0.1
        )

        control_timeout = (
            state.last_control_time is None
            or now - state.last_control_time > 0.2
        )

        if imu_timeout or control_timeout:
            state.safety_ok = False
            state.log("safety_task", "safety fault detected")
        else:
            state.safety_ok = True

        state.safety_count += 1

        next_time = await wait_next_period(next_time, SAFETY_PERIOD_SEC)


async def heartbeat_task(state):
    next_time = time.monotonic()
    led_on = False

    while state.should_run():
        led_on = not led_on
        state.heartbeat_count += 1

        print(f"[HEARTBEAT] t={state.now():.2f}s | LED={'ON' if led_on else 'OFF'}")

        state.log("heartbeat_task", "toggle led")

        next_time = await wait_next_period(next_time, HEARTBEAT_PERIOD_SEC)


def save_log(state):
    log_path = Path.home() / "uav-learning" / "data" / "month3" / "freertos_task_log.csv"
    log_path.parent.mkdir(parents=True, exist_ok=True)

    with open(log_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        writer.writerow([
            "time_sec",
            "task_name",
            "message",
            "imu_count",
            "attitude_count",
            "control_count",
            "telemetry_count",
            "safety_count",
            "heartbeat_count",
            "safety_ok",
        ])

        writer.writerows(state.log_rows)

    print()
    print(f"Log saved to: {log_path}")


async def main():
    state = SystemState()

    imu_queue = asyncio.Queue(maxsize=1)
    attitude_queue = asyncio.Queue(maxsize=1)

    tasks = [
        asyncio.create_task(imu_task(state, imu_queue)),
        asyncio.create_task(attitude_task(state, imu_queue, attitude_queue)),
        asyncio.create_task(control_task(state, attitude_queue)),
        asyncio.create_task(telemetry_task(state)),
        asyncio.create_task(safety_task(state)),
        asyncio.create_task(heartbeat_task(state)),
    ]

    await asyncio.gather(*tasks)

    save_log(state)

    print()
    print("Task count summary:")
    print(f"  imu_task:       {state.imu_count}")
    print(f"  attitude_task:  {state.attitude_count}")
    print(f"  control_task:   {state.control_count}")
    print(f"  telemetry_task: {state.telemetry_count}")
    print(f"  safety_task:    {state.safety_count}")
    print(f"  heartbeat_task: {state.heartbeat_count}")


if __name__ == "__main__":
    asyncio.run(main())
