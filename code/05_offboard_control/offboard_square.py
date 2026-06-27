import asyncio
from pathlib import Path

from mavsdk.offboard import PositionNedYaw

from offboard_utils import (
    TelemetryLogger,
    SetpointStreamer,
    action_takeoff,
    connect_drone,
    hold_setpoint,
    safe_land,
    start_offboard,
    wait_until_health_ok,
)


async def main():
    drone = await connect_drone()

    csv_path = Path.home() / "uav-learning" / "data" / "month3" / "offboard_square.csv"
    logger = TelemetryLogger(drone, csv_path)
    await logger.start()

    streamer = None

    waypoints = [
        ("P0_START", 0.0, 0.0, -3.0, 0.0),
        ("P1_NORTH", 3.0, 0.0, -3.0, 0.0),
        ("P2_NORTH_EAST", 3.0, 3.0, -3.0, 0.0),
        ("P3_EAST", 0.0, 3.0, -3.0, 0.0),
        ("P4_RETURN", 0.0, 0.0, -3.0, 0.0),
    ]

    try:
        logger.set_phase("WAITING_HEALTH")
        await wait_until_health_ok(drone)

        logger.set_phase("TAKEOFF")
        await action_takeoff(drone, target_altitude_m=3.0)

        initial_setpoint = PositionNedYaw(0.0, 0.0, -3.0, 0.0)
        streamer = SetpointStreamer(drone, initial_setpoint)

        logger.set_phase("STARTING_OFFBOARD")
        await start_offboard(drone, streamer)

        for phase, north, east, down, yaw in waypoints:
            await hold_setpoint(
                streamer,
                logger,
                north_m=north,
                east_m=east,
                down_m=down,
                yaw_deg=yaw,
                duration_sec=8.0,
                phase=phase,
            )

    except Exception as error:
        print(f"[ERROR] {error}")

    finally:
        await safe_land(drone, logger, streamer)
        await asyncio.sleep(8)
        logger.set_phase("FINISHED")
        await logger.stop()


if __name__ == "__main__":
    asyncio.run(main())
