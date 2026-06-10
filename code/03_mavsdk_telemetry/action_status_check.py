import asyncio
from mavsdk import System


async def wait_for_connection(drone: System) -> None:
    print("Waiting for PX4 connection...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            return


async def get_one_armed_state(drone: System) -> bool:
    async for armed in drone.telemetry.armed():
        return armed


async def get_one_flight_mode(drone: System) -> str:
    async for flight_mode in drone.telemetry.flight_mode():
        return str(flight_mode)


async def get_one_position(drone: System):
    async for position in drone.telemetry.position():
        return position


async def main():
    drone = System()

    print("Connecting to PX4 SITL on udp://:14540 ...")
    await drone.connect(system_address="udp://:14540")

    await wait_for_connection(drone)

    armed = await get_one_armed_state(drone)
    flight_mode = await get_one_flight_mode(drone)
    position = await get_one_position(drone)

    print("\n===== Action Status Check =====")
    print(f"Armed: {armed}")
    print(f"Flight mode: {flight_mode}")
    print(f"Relative altitude: {position.relative_altitude_m:.3f} m")
    print("\nAction plugin is ready to be used in the next task.")
    print("Today we do not arm or take off.")


if __name__ == "__main__":
    asyncio.run(main())
