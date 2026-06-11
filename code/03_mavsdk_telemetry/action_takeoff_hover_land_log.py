import asyncio
import csv
import os
import time
from mavsdk import System
from mavsdk.action import ActionError


TAKEOFF_ALTITUDE_M = 3.0
ALTITUDE_TOLERANCE_M = 0.5
HOVER_TIME_S = 10
LOG_INTERVAL_S = 0.2
MAX_TAKEOFF_WAIT_S = 30.0
MAX_LAND_WAIT_S = 40.0
OUTPUT_CSV = "data/takeoff_hover_land_telemetry.csv"


async def wait_for_connection(drone: System) -> None:
    print("Waiting for PX4 connection...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            return


async def wait_until_ready(drone: System) -> None:
    print("Waiting for drone health...")

    async for health in drone.telemetry.health():
        print(
            "Health | "
            f"global_position_ok={health.is_global_position_ok} | "
            f"home_position_ok={health.is_home_position_ok}"
        )

        if health.is_global_position_ok and health.is_home_position_ok:
            print("Drone is ready.")
            return

        await asyncio.sleep(1.0)


async def observe_position(drone: System, latest: dict) -> None:
    async for position in drone.telemetry.position():
        latest["latitude_deg"] = position.latitude_deg
        latest["longitude_deg"] = position.longitude_deg
        latest["absolute_altitude_m"] = position.absolute_altitude_m
        latest["relative_altitude_m"] = position.relative_altitude_m


async def observe_attitude(drone: System, latest: dict) -> None:
    async for attitude in drone.telemetry.attitude_euler():
        latest["roll_deg"] = attitude.roll_deg
        latest["pitch_deg"] = attitude.pitch_deg
        latest["yaw_deg"] = attitude.yaw_deg


async def observe_flight_mode(drone: System, latest: dict) -> None:
    async for flight_mode in drone.telemetry.flight_mode():
        latest["flight_mode"] = str(flight_mode)


async def observe_armed(drone: System, latest: dict) -> None:
    async for armed in drone.telemetry.armed():
        latest["armed"] = armed


def safe_value(value):
    if value is None:
        return ""
    return value


async def wait_until_latest_has_altitude(latest: dict) -> None:
    print("Waiting for first altitude telemetry...")

    while latest.get("relative_altitude_m") is None:
        await asyncio.sleep(0.1)

    print("Altitude telemetry received.")


async def log_telemetry_csv(latest: dict, stop_event: asyncio.Event) -> None:
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    fieldnames = [
        "time_s",
        "mission_phase",
        "armed",
        "flight_mode",
        "latitude_deg",
        "longitude_deg",
        "absolute_altitude_m",
        "relative_altitude_m",
        "roll_deg",
        "pitch_deg",
        "yaw_deg",
    ]

    start_time = time.time()

    with open(OUTPUT_CSV, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while not stop_event.is_set():
            elapsed = time.time() - start_time

            row = {
                "time_s": round(elapsed, 3),
                "mission_phase": safe_value(latest.get("mission_phase")),
                "armed": safe_value(latest.get("armed")),
                "flight_mode": safe_value(latest.get("flight_mode")),
                "latitude_deg": safe_value(latest.get("latitude_deg")),
                "longitude_deg": safe_value(latest.get("longitude_deg")),
                "absolute_altitude_m": safe_value(latest.get("absolute_altitude_m")),
                "relative_altitude_m": safe_value(latest.get("relative_altitude_m")),
                "roll_deg": safe_value(latest.get("roll_deg")),
                "pitch_deg": safe_value(latest.get("pitch_deg")),
                "yaw_deg": safe_value(latest.get("yaw_deg")),
            }

            writer.writerow(row)
            csv_file.flush()

            print(
                f"LOG | t={elapsed:5.1f}s | "
                f"phase={row['mission_phase']} | "
                f"mode={row['flight_mode']} | "
                f"armed={row['armed']} | "
                f"alt={row['relative_altitude_m']} | "
                f"roll={row['roll_deg']} | "
                f"pitch={row['pitch_deg']} | "
                f"yaw={row['yaw_deg']}"
            )

            await asyncio.sleep(LOG_INTERVAL_S)

    print(f"\nTelemetry saved to: {OUTPUT_CSV}")


async def wait_for_takeoff_altitude(latest: dict) -> None:
    print("\nWaiting for takeoff altitude...")

    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        altitude = latest.get("relative_altitude_m")

        if altitude is not None:
            print(f"TAKEOFF | t={elapsed:5.1f}s | relative_altitude={altitude:.2f} m")

            if altitude >= TAKEOFF_ALTITUDE_M - ALTITUDE_TOLERANCE_M:
                print("Target takeoff altitude reached.")
                return

        if elapsed > MAX_TAKEOFF_WAIT_S:
            print("Timeout: takeoff altitude was not reached.")
            return

        await asyncio.sleep(0.5)


async def hover(latest: dict) -> None:
    print(f"\nHovering for {HOVER_TIME_S} seconds...")

    latest["mission_phase"] = "hover"

    for second in range(HOVER_TIME_S):
        altitude = latest.get("relative_altitude_m")
        roll = latest.get("roll_deg")
        pitch = latest.get("pitch_deg")
        yaw = latest.get("yaw_deg")

        print(
            f"HOVER | {second + 1:02d}/{HOVER_TIME_S}s | "
            f"alt={altitude} | roll={roll} | pitch={pitch} | yaw={yaw}"
        )

        await asyncio.sleep(1.0)

    print("Hover finished.")


async def wait_for_landing(latest: dict) -> None:
    print("\nWaiting for landing...")

    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        altitude = latest.get("relative_altitude_m")

        if altitude is not None:
            print(f"LAND | t={elapsed:5.1f}s | relative_altitude={altitude:.2f} m")

            if altitude <= 0.15 and elapsed > 3.0:
                print("Drone is near ground. Landing is likely complete.")
                return

        if elapsed > MAX_LAND_WAIT_S:
            print("Timeout: landing was not confirmed by altitude.")
            return

        await asyncio.sleep(0.5)


async def run_mission(drone: System, latest: dict) -> None:
    await wait_until_ready(drone)
    await wait_until_latest_has_altitude(latest)

    try:
        latest["mission_phase"] = "set_takeoff_altitude"
        print(f"\nSetting takeoff altitude to {TAKEOFF_ALTITUDE_M} m...")
        await drone.action.set_takeoff_altitude(TAKEOFF_ALTITUDE_M)

        latest["mission_phase"] = "arming"
        print("Arming...")
        await drone.action.arm()
        print("Armed successfully.")

        latest["mission_phase"] = "takeoff"
        print("Taking off...")
        await drone.action.takeoff()
        print("Takeoff command sent.")

        await wait_for_takeoff_altitude(latest)

        await hover(latest)

        latest["mission_phase"] = "landing"
        print("\nLanding...")
        await drone.action.land()
        print("Land command sent.")

        await wait_for_landing(latest)

        latest["mission_phase"] = "finished"
        print("\nMission finished.")
        print("Completed: arm -> takeoff -> hover -> land")

    except ActionError as error:
        latest["mission_phase"] = "action_error"
        print("\nAction failed.")
        print(error)


async def main() -> None:
    drone = System()
    latest = {"mission_phase": "init"}
    stop_event = asyncio.Event()

    print("Connecting to PX4 SITL on udp://:14540 ...")
    await drone.connect(system_address="udp://:14540")

    await wait_for_connection(drone)

    observer_tasks = [
        asyncio.create_task(observe_position(drone, latest)),
        asyncio.create_task(observe_attitude(drone, latest)),
        asyncio.create_task(observe_flight_mode(drone, latest)),
        asyncio.create_task(observe_armed(drone, latest)),
    ]

    logger_task = asyncio.create_task(log_telemetry_csv(latest, stop_event))

    try:
        await run_mission(drone, latest)

    except KeyboardInterrupt:
        latest["mission_phase"] = "interrupted"
        print("\nProgram interrupted by user.")

    finally:
        print("\nStopping logger...")
        stop_event.set()
        await logger_task

        for task in observer_tasks:
            task.cancel()

        await asyncio.gather(*observer_tasks, return_exceptions=True)

        print("All telemetry tasks stopped.")


if __name__ == "__main__":
    asyncio.run(main())
