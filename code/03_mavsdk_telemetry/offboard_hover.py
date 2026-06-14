import asyncio
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk.offboard import OffboardError, PositionNedYaw


TAKEOFF_ALTITUDE_M = 3.0
TARGET_ALTITUDE_M = 3.0
ALTITUDE_TOLERANCE_M = 0.5
HOVER_TIME_S = 10


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


async def wait_for_takeoff_altitude(drone: System) -> None:
    print("\nWaiting for takeoff altitude...")

    async for position in drone.telemetry.position():
        altitude = position.relative_altitude_m
        print(f"relative_altitude={altitude:.2f} m")

        if altitude >= TAKEOFF_ALTITUDE_M - ALTITUDE_TOLERANCE_M:
            print("Takeoff altitude reached.")
            return

        await asyncio.sleep(0.5)


async def print_position_for_seconds(drone: System, seconds: int) -> None:
    start_time = asyncio.get_event_loop().time()

    async for position in drone.telemetry.position():
        elapsed = asyncio.get_event_loop().time() - start_time

        print(
            f"t={elapsed:5.1f}s | "
            f"relative_altitude={position.relative_altitude_m:.2f} m"
        )

        if elapsed >= seconds:
            return

        await asyncio.sleep(1.0)


async def main() -> None:
    drone = System()

    print("Connecting to PX4 SITL on udp://:14540 ...")
    await drone.connect(system_address="udp://:14540")

    await wait_for_connection(drone)
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

        print("\nSending initial Offboard setpoint...")
        await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 0.0, -TARGET_ALTITUDE_M, 0.0)
        )

        print("Starting Offboard...")
        await drone.offboard.start()
        print("Offboard started.")

        print(f"\nHolding position for {HOVER_TIME_S} seconds...")
        await print_position_for_seconds(drone, HOVER_TIME_S)

        print("\nStopping Offboard...")
        await drone.offboard.stop()
        print("Offboard stopped.")

        print("Landing...")
        await drone.action.land()
        print("Land command sent.")

    except OffboardError as error:
        print("\nOffboard failed.")
        print(error)
        print("Trying to land...")
        await drone.action.land()

    except ActionError as error:
        print("\nAction failed.")
        print(error)

    except KeyboardInterrupt:
        print("\nProgram interrupted.")
        print("Trying to land...")
        await drone.action.land()


if __name__ == "__main__":
    asyncio.run(main())
