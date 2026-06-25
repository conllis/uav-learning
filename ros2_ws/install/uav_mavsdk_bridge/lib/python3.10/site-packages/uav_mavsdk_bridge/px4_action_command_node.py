import asyncio
import threading

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from mavsdk import System


CONNECTION_URL = "udp://:14540"


class PX4ActionCommandNode(Node):
    def __init__(self):
        super().__init__('px4_action_command_node')

        self.drone = None
        self.loop = None
        self.is_connected = False
        self.takeoff_sent = False

        self.command_subscription = self.create_subscription(
            String,
            '/uav/action_command',
            self.command_callback,
            10
        )

        self.mavsdk_thread = threading.Thread(
            target=self.start_mavsdk_loop,
            daemon=True
        )
        self.mavsdk_thread.start()

        self.get_logger().info('PX4 action command node started.')
        self.get_logger().info('Supported commands: status, takeoff, land')

    def start_mavsdk_loop(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        self.loop.run_until_complete(self.connect_px4())
        self.loop.run_forever()

    async def connect_px4(self):
        self.drone = System()

        self.get_logger().info(f'Connecting to PX4 via {CONNECTION_URL} ...')
        await self.drone.connect(system_address=CONNECTION_URL)

        async for state in self.drone.core.connection_state():
            if state.is_connected:
                self.is_connected = True
                self.get_logger().info('PX4 discovered and connected.')
                break

    def command_callback(self, msg):
        command = msg.data.strip().lower()

        self.get_logger().info(f'Received command: {command}')

        if self.loop is None or not self.is_connected:
            self.get_logger().warn('PX4 is not connected yet. Please wait.')
            return

        if command == 'status':
            asyncio.run_coroutine_threadsafe(
                self.print_status(),
                self.loop
            )
        elif command == 'takeoff':
            asyncio.run_coroutine_threadsafe(
                self.takeoff(),
                self.loop
            )
        elif command == 'land':
            asyncio.run_coroutine_threadsafe(
                self.land(),
                self.loop
            )
        else:
            self.get_logger().warn(
                f'Unknown command: {command}. Use status, takeoff, or land.'
            )

    async def get_one(self, telemetry_stream):
        async for item in telemetry_stream:
            return item

    async def print_status(self):
        try:
            health = await self.get_one(self.drone.telemetry.health())
            in_air = await self.get_one(self.drone.telemetry.in_air())
            flight_mode = await self.get_one(self.drone.telemetry.flight_mode())
            position = await self.get_one(self.drone.telemetry.position())
            attitude = await self.get_one(self.drone.telemetry.attitude_euler())

            self.get_logger().info('===== PX4 STATUS =====')
            self.get_logger().info(f'connected: {self.is_connected}')
            self.get_logger().info(f'in_air: {in_air}')
            self.get_logger().info(f'flight_mode: {flight_mode}')
            self.get_logger().info(
                f'health: global_position_ok={health.is_global_position_ok}, '
                f'home_position_ok={health.is_home_position_ok}'
            )
            self.get_logger().info(
                f'altitude: relative={position.relative_altitude_m:.2f} m, '
                f'absolute={position.absolute_altitude_m:.2f} m'
            )
            self.get_logger().info(
                f'attitude: roll={attitude.roll_deg:.2f} deg, '
                f'pitch={attitude.pitch_deg:.2f} deg, '
                f'yaw={attitude.yaw_deg:.2f} deg'
            )
            self.get_logger().info('======================')

        except Exception as error:
            self.get_logger().error(f'Failed to get status: {error}')

    async def takeoff(self):
        try:
            if self.takeoff_sent:
                self.get_logger().warn('Takeoff command was already sent. Ignored.')
                return

            health = await self.get_one(self.drone.telemetry.health())

            if not health.is_global_position_ok or not health.is_home_position_ok:
                self.get_logger().warn(
                    'PX4 health check is not ready. '
                    'Global position or home position is not OK.'
                )
                return

            self.get_logger().info('Setting takeoff altitude to 3 m...')
            await self.drone.action.set_takeoff_altitude(3.0)

            self.get_logger().info('Arming...')
            await self.drone.action.arm()

            self.get_logger().info('Taking off...')
            await self.drone.action.takeoff()

            self.takeoff_sent = True
            self.get_logger().info('Takeoff command sent.')

        except Exception as error:
            self.get_logger().error(f'Takeoff failed: {error}')

    async def land(self):
        try:
            self.get_logger().info('Landing...')
            await self.drone.action.land()
            self.get_logger().info('Land command sent.')

        except Exception as error:
            self.get_logger().error(f'Land failed: {error}')


def main(args=None):
    rclpy.init(args=args)

    node = PX4ActionCommandNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
