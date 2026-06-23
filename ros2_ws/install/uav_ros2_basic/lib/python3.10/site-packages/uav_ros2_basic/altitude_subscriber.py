import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class AltitudeSubscriber(Node):
    def __init__(self):
        super().__init__('altitude_subscriber')

        self.subscription = self.create_subscription(
            Float32,
            '/uav/relative_altitude',
            self.altitude_callback,
            10
        )

        self.get_logger().info('Altitude subscriber node started.')

    def altitude_callback(self, msg):
        self.get_logger().info(
            f'Received altitude: {msg.data:.2f} m'
        )


def main(args=None):
    rclpy.init(args=args)

    node = AltitudeSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
