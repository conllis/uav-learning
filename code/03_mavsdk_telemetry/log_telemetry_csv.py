import asyncio
import csv
import os
import time
from mavsdk import System


async def wait_for_connection(drone: System) -> None:
    print("Waiting for PX4 connection...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            return


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


async def log_csv(latest: dict, output_path: str, duration_s: int = 30, interval_s: float = 0.2) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    fieldnames = [
        "time_s",
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

    with open(output_path, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        while True:
            elapsed = time.time() - start_time
            if elapsed > duration_s:
                break

            row = {
                "time_s": round(elapsed, 3),
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

            print(
                f"t={elapsed:5.2f}s | "
                f"mode={row['flight_mode']} | "
                f"armed={row['armed']} | "
                f"rel_alt={row['relative_altitude_m']} | "
                f"roll={row['roll_deg']} | "
                f"pitch={row['pitch_deg']} | "
                f"yaw={row['yaw_deg']}"
            )

            await asyncio.sleep(interval_s)

    print(f"\nTelemetry saved to: {output_path}")


async def main():
    drone = System()

    print("Connecting to PX4 SITL on udp://:14540 ...")
    await drone.connect(system_address="udp://:14540")

    await wait_for_connection(drone)

    latest = {}

    tasks = [
        asyncio.create_task(observe_position(drone, latest)),
        asyncio.create_task(observe_attitude(drone, latest)),
        asyncio.create_task(observe_flight_mode(drone, latest)),
        asyncio.create_task(observe_armed(drone, latest)),
    ]

    try:
        await log_csv(
            latest=latest,
            output_path="data/px4_telemetry.csv",
            duration_s=30,
            interval_s=0.2,
        )
    finally:
        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

    print("CSV logging finished.")


if __name__ == "__main__":
    asyncio.run(main())

