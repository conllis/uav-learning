import asyncio
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


def format_value(value, digits=3):
    if value is None:
        return "N/A"

    if isinstance(value, float):
        return f"{value:.{digits}f}"

    return str(value)


async def print_telemetry(latest: dict, duration_s: int = 30) -> None:
    for _ in range(duration_s):
        print("\n----- PX4 Basic Telemetry -----")
        print(f"Armed:          {format_value(latest.get('armed'))}")
        print(f"Flight mode:    {format_value(latest.get('flight_mode'))}")
        print(f"Latitude:       {format_value(latest.get('latitude_deg'), 7)} deg")
        print(f"Longitude:      {format_value(latest.get('longitude_deg'), 7)} deg")
        print(f"Abs altitude:   {format_value(latest.get('absolute_altitude_m'))} m")
        print(f"Rel altitude:   {format_value(latest.get('relative_altitude_m'))} m")
        print(f"Roll:           {format_value(latest.get('roll_deg'))} deg")
        print(f"Pitch:          {format_value(latest.get('pitch_deg'))} deg")
        print(f"Yaw:            {format_value(latest.get('yaw_deg'))} deg")

        await asyncio.sleep(1.0)


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
        await print_telemetry(latest, duration_s=30)
    finally:
        for task in tasks:
            task.cancel()

        await asyncio.gather(*tasks, return_exceptions=True)

    print("\nTelemetry reading finished.")


if __name__ == "__main__":
    asyncio.run(main())
