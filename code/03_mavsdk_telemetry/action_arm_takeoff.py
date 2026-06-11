import asyncio
from mavsdk import System
from mavsdk.action import ActionError


TAKEOFF_ALTITUDE_M = 3.0
ALTITUDE_TOLERANCE_M = 0.5
MAX_TAKEOFF_WAIT_S = 30.0


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


async def get_one_status(drone: System) -> None:
    armed = None
    flight_mode = None
    altitude = None

    async for armed_value in drone.telemetry.armed():
        armed = armed_value
        break

    async for mode in drone.telemetry.flight_mode():
        flight_mode = mode
        break

    async for position in drone.telemetry.position():
        altitude = position.relative_altitude_m
        break

    print("\n===== Current PX4 Status =====")
    print(f"Armed: {armed}")
    print(f"Flight mode: {flight_mode}")
    print(f"Relative altitude: {altitude:.3f} m")


async def wait_for_takeoff_altitude(drone: System) -> None:
    print("\nWaiting for takeoff altitude...")

    start_time = asyncio.get_event_loop().time()

    async for position in drone.telemetry.position():
        now = asyncio.get_event_loop().time()
        elapsed = now - start_time
        altitude = position.relative_altitude_m

        print(f"t={elapsed:5.1f}s | relative_altitude={altitude:.2f} m")

        if altitude >= TAKEOFF_ALTITUDE_M - ALTITUDE_TOLERANCE_M:
            print("Target takeoff altitude reached.")
            return

        if elapsed > MAX_TAKEOFF_WAIT_S:
            print("Timeout: takeoff altitude was not reached.")
            return


async def main() -> None:
    drone = System()

    print("Connecting to PX4 SITL on udp://:14540 ...")
    await drone.connect(system_address="udp://:14540")

    await wait_for_connection(drone)
    await get_one_status(drone)
    await wait_until_ready(drone)

    try:
        print(f"\nSetting takeoff altitude to {TAKEOFF_ALTITUDE_M} m...")
        await drone.action.set_takeoff_altitude(TAKEOFF_ALTITUDE_M)

        print("Arming...")
        await drone.action.arm()
        print("Armed successfully.")

        print("Taking off...")
        await drone.action.takeoff()
        print("Takeoff command sent.")

        await wait_for_takeoff_altitude(drone)

        print("\nHovering for 8 seconds...")
        await asyncio.sleep(8)

        await get_one_status(drone)

        print("\nDay 46 test finished.")
        print("The drone should now be hovering in PX4 SITL.")
        print("Please land manually using QGroundControl or PX4 shell: commander land")

    except ActionError as error:
        print("\nAction failed.")
        print(error)

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")


if __name__ == "__main__":
    asyncio.run(main())
