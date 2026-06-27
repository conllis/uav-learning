import asyncio
import csv
import time
from pathlib import Path

from mavsdk import System
from mavsdk.offboard import OffboardError, PositionNedYaw


CONNECTION_URL = "udpin://0.0.0.0:14540"


class TelemetryLogger:
    def __init__(self, drone, csv_path):
        self.drone = drone
        self.csv_path = Path(csv_path)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

        self.start_time = time.time()
        self.phase = "INIT"
        self.running = True
        self.tasks = []

        self.data = {
            "relative_altitude_m": None,
            "roll_deg": None,
            "pitch_deg": None,
            "yaw_deg": None,
            "north_m": None,
            "east_m": None,
            "down_m": None,
            "flight_mode": None,
        }

        self.csv_file = open(self.csv_path, mode="w", newline="")
        self.writer = csv.writer(self.csv_file)

        self.writer.writerow([
            "time_sec",
            "relative_altitude_m",
            "roll_deg",
            "pitch_deg",
            "yaw_deg",
            "north_m",
            "east_m",
            "down_m",
            "flight_mode",
            "mission_phase",
        ])

    def set_phase(self, phase):
        self.phase = phase
        print(f"[PHASE] {phase}")

    async def start(self):
        self.tasks = [
            asyncio.create_task(self.read_position()),
            asyncio.create_task(self.read_attitude()),
            asyncio.create_task(self.read_position_velocity_ned()),
            asyncio.create_task(self.read_flight_mode()),
            asyncio.create_task(self.write_loop()),
        ]

    async def stop(self):
        self.running = False

        for task in self.tasks:
            task.cancel()

        await asyncio.sleep(0.2)

        self.csv_file.flush()
        self.csv_file.close()

        print(f"[LOGGER] CSV saved to: {self.csv_path}")

    async def read_position(self):
        async for position in self.drone.telemetry.position():
            self.data["relative_altitude_m"] = position.relative_altitude_m

    async def read_attitude(self):
        async for attitude in self.drone.telemetry.attitude_euler():
            self.data["roll_deg"] = attitude.roll_deg
            self.data["pitch_deg"] = attitude.pitch_deg
            self.data["yaw_deg"] = attitude.yaw_deg

    async def read_position_velocity_ned(self):
        async for pv in self.drone.telemetry.position_velocity_ned():
            self.data["north_m"] = pv.position.north_m
            self.data["east_m"] = pv.position.east_m
            self.data["down_m"] = pv.position.down_m

    async def read_flight_mode(self):
        async for flight_mode in self.drone.telemetry.flight_mode():
            self.data["flight_mode"] = str(flight_mode)

    async def write_loop(self):
        while self.running:
            elapsed = time.time() - self.start_time

            row = [
                f"{elapsed:.3f}",
                value_or_empty(self.data["relative_altitude_m"]),
                value_or_empty(self.data["roll_deg"]),
                value_or_empty(self.data["pitch_deg"]),
                value_or_empty(self.data["yaw_deg"]),
                value_or_empty(self.data["north_m"]),
                value_or_empty(self.data["east_m"]),
                value_or_empty(self.data["down_m"]),
                self.data["flight_mode"] if self.data["flight_mode"] else "",
                self.phase,
            ]

            self.writer.writerow(row)
            self.csv_file.flush()

            await asyncio.sleep(0.2)


def value_or_empty(value):
    if value is None:
        return ""
    return f"{value:.3f}"


class SetpointStreamer:
    def __init__(self, drone, initial_setpoint):
        self.drone = drone
        self.current_setpoint = initial_setpoint
        self.running = False
        self.task = None

    def update(self, north_m, east_m, down_m, yaw_deg=0.0):
        self.current_setpoint = PositionNedYaw(
            north_m,
            east_m,
            down_m,
            yaw_deg,
        )

        print(
            f"[SETPOINT] north={north_m:.2f}, "
            f"east={east_m:.2f}, down={down_m:.2f}, yaw={yaw_deg:.2f}"
        )

    async def start(self):
        self.running = True
        self.task = asyncio.create_task(self.loop())

    async def stop(self):
        self.running = False

        if self.task is not None:
            await asyncio.sleep(0.2)
            self.task.cancel()

    async def loop(self):
        while self.running:
            await self.drone.offboard.set_position_ned(self.current_setpoint)
            await asyncio.sleep(0.05)


async def connect_drone():
    drone = System()

    print(f"[CONNECT] Connecting to PX4 via {CONNECTION_URL} ...")
    await drone.connect(system_address=CONNECTION_URL)

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("[CONNECT] PX4 discovered and connected.")
            return drone


async def wait_until_health_ok(drone, timeout_sec=40):
    print("[HEALTH] Waiting for PX4 health check...")

    start = time.time()

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("[HEALTH] PX4 health OK.")
            return

        if time.time() - start > timeout_sec:
            raise TimeoutError("PX4 health check timeout.")

        await asyncio.sleep(0.5)


async def wait_until_altitude(drone, target_altitude_m, timeout_sec=30):
    print(f"[TAKEOFF] Waiting until local altitude reaches {target_altitude_m:.1f} m...")

    start = time.time()

    while True:
        position = await get_one(drone.telemetry.position())
        pv_ned = await get_one(drone.telemetry.position_velocity_ned())
        in_air = await get_one(drone.telemetry.in_air())
        flight_mode = await get_one(drone.telemetry.flight_mode())
        armed = await get_one(drone.telemetry.armed())

        relative_altitude = position.relative_altitude_m
        local_altitude = -pv_ned.position.down_m

        print(
            f"[ALTITUDE] relative={relative_altitude:.2f} m | "
            f"local_ned={local_altitude:.2f} m | "
            f"down={pv_ned.position.down_m:.2f} m | "
            f"in_air={in_air} | armed={armed} | mode={flight_mode}"
        )

        if local_altitude >= target_altitude_m * 0.75:
            print("[TAKEOFF] Local altitude reached enough for Offboard handover.")
            return

        if time.time() - start > timeout_sec:
            raise TimeoutError("Waiting for takeoff altitude timeout.")

        await asyncio.sleep(0.5)


async def action_takeoff(drone, target_altitude_m=3.0):
    print("[ACTION] Setting takeoff altitude...")
    await drone.action.set_takeoff_altitude(target_altitude_m)

    print("[ACTION] Arming...")
    await drone.action.arm()

    print("[ACTION] Taking off...")
    await drone.action.takeoff()

    await wait_until_altitude(drone, target_altitude_m)


async def start_offboard(drone, streamer):
    print("[OFFBOARD] Sending initial setpoints...")

    for _ in range(20):
        await drone.offboard.set_position_ned(streamer.current_setpoint)
        await asyncio.sleep(0.05)

    await streamer.start()

    print("[OFFBOARD] Starting Offboard mode...")

    try:
        await drone.offboard.start()
        print("[OFFBOARD] Offboard mode started.")
    except OffboardError as error:
        print(f"[OFFBOARD] Failed to start Offboard: {error}")
        raise


async def hold_setpoint(streamer, logger, north_m, east_m, down_m, yaw_deg, duration_sec, phase):
    logger.set_phase(phase)
    streamer.update(north_m, east_m, down_m, yaw_deg)

    start = time.time()

    while time.time() - start < duration_sec:
        await asyncio.sleep(0.5)


async def safe_land(drone, logger=None, streamer=None):
    print("[LAND] Starting safe landing...")

    if logger is not None:
        logger.set_phase("LANDING")

    if streamer is not None:
        try:
            await streamer.stop()
        except Exception as error:
            print(f"[LAND] Failed to stop streamer: {error}")

    try:
        await drone.offboard.stop()
        print("[LAND] Offboard stopped.")
    except Exception:
        pass

    try:
        await drone.action.land()
        print("[LAND] Land command sent.")
    except Exception as error:
        print(f"[LAND] Land failed: {error}")
async def get_one(telemetry_stream):
    async for item in telemetry_stream:
        return item
