import asyncio
from mavsdk import System
from mavsdk.action import ActionError
from mavsdk.offboard import OffboardError, PositionNedYaw


TAKEOFF_ALTITUDE_M = 3.0
ALTITUDE_TOLERANCE_M = 0.5

START_X_M = 0.0
START_Y_M = 0.0
TARGET_Z_M = -3.0

TARGET_X_M = 3.0
TARGET_Y_M = 0.0
TARGET_YAW_DEG = 0.0

HOVER_BEFORE_MOVE_S = 5
MOVE_HOLD_S = 10


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


async def hold_current_setpoint(seconds: int, label: str) -> None:
    for i in range(seconds):
        print(f"{label}: {i + 1}/{seconds} s")
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

        print("\nSending initial Offboard setpoint: hover at 3 m...")
        await drone.offboard.set_position_ned(
            PositionNedYaw(
                START_X_M,
                START_Y_M,
                TARGET_Z_M,
                TARGET_YAW_DEG,
            )
        )

        print("Starting Offboard...")
        await drone.offboard.start()
        print("Offboard started.")

        print("\nOffboard hover before move...")
        await hold_current_setpoint(HOVER_BEFORE_MOVE_S, "HOVER")

        print("\nSending move setpoint...")
        print(
            f"Target point: x={TARGET_X_M} m, "
            f"y={TARGET_Y_M} m, z={TARGET_Z_M} m, yaw={TARGET_YAW_DEG} deg"
        )

        await drone.offboard.set_position_ned(
            PositionNedYaw(
                TARGET_X_M,
                TARGET_Y_M,
                TARGET_Z_M,
                TARGET_YAW_DEG,
            )
        )

        print("\nHolding target point...")
        await hold_current_setpoint(MOVE_HOLD_S, "MOVE TARGET HOLD")

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
