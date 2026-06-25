import asyncio
import threading

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_msgs.msg import String

from mavsdk import System


CONNECTION_URL = "udp://:14540"


class PX4TelemetryBridge(Node):
    def __init__(self):
        super().__init__('px4_telemetry_bridge')

        self.altitude_pub = self.create_publisher(
            Float32,
            '/px4/relative_altitude',
            10
        )

        self.roll_pub = self.create_publisher(
            Float32,
            '/px4/roll',
            10
        )

        self.pitch_pub = self.create_publisher(
            Float32,
            '/px4/pitch',
            10
        )

        self.yaw_pub = self.create_publisher(
            Float32,
            '/px4/yaw',
            10
        )

        self.flight_mode_pub = self.create_publisher(
            String,
            '/px4/flight_mode',
            10
        )

        self.latest_altitude = None
        self.latest_roll = None
        self.latest_pitch = None
        self.latest_yaw = None
        self.latest_flight_mode = None

        self.data_lock = threading.Lock()

        self.publish_timer = self.create_timer(
            0.2,
            self.publish_latest_telemetry
        )

        self.mavsdk_thread = threading.Thread(
            target=self.run_mavsdk_loop,
            daemon=True
        )
        self.mavsdk_thread.start()

        self.get_logger().info('PX4 telemetry bridge node started.')

    def run_mavsdk_loop(self):
        asyncio.run(self.mavsdk_main())

    async def mavsdk_main(self):
        drone = System()

        self.get_logger().info(f'Connecting to PX4 via {CONNECTION_URL} ...')
        await drone.connect(system_address=CONNECTION_URL)

        async for state in drone.core.connection_state():
            if state.is_connected:
                self.get_logger().info('PX4 discovered and connected.')
                break

        await asyncio.gather(
            self.read_position(drone),
            self.read_attitude(drone),
            self.read_flight_mode(drone)
        )

    async def read_position(self, drone):
        async for position in drone.telemetry.position():
            with self.data_lock:
                self.latest_altitude = float(position.relative_altitude_m)

    async def read_attitude(self, drone):
        async for attitude in drone.telemetry.attitude_euler():
            with self.data_lock:
                self.latest_roll = float(attitude.roll_deg)
                self.latest_pitch = float(attitude.pitch_deg)
                self.latest_yaw = float(attitude.yaw_deg)

    async def read_flight_mode(self, drone):
        async for flight_mode in drone.telemetry.flight_mode():
            with self.data_lock:
                self.latest_flight_mode = str(flight_mode)

    def publish_latest_telemetry(self):
        with self.data_lock:
            altitude = self.latest_altitude
            roll = self.latest_roll
            pitch = self.latest_pitch
            yaw = self.latest_yaw
            flight_mode = self.latest_flight_mode

        if altitude is not None:
            msg = Float32()
            msg.data = altitude
            self.altitude_pub.publish(msg)

        if roll is not None:
            msg = Float32()
            msg.data = roll
            self.roll_pub.publish(msg)

        if pitch is not None:
            msg = Float32()
            msg.data = pitch
            self.pitch_pub.publish(msg)

        if yaw is not None:
            msg = Float32()
            msg.data = yaw
            self.yaw_pub.publish(msg)

        if flight_mode is not None:
            msg = String()
            msg.data = flight_mode
            self.flight_mode_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    node = PX4TelemetryBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
