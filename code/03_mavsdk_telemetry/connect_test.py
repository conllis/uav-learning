import asyncio
from mavsdk import System


async def main():
    # 创建一个无人机系统对象
    drone = System()

    # 连接 PX4 SITL。
    # Day 39 中 mavlink status 显示：
    # PX4 instance #1: UDP local 14580, remote port 14540, mode Onboard
    # 所以这里监听 14540。
    print("Connecting to PX4 SITL on udp://:14540 ...")
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone connection...")

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Drone connected!")
            break

    print("Connection test finished.")


if __name__ == "__main__":
    asyncio.run(main())
