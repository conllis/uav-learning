import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class AltitudePublisher(Node):
    def __init__(self):
        super().__init__('altitude_publisher')

        self.publisher_ = self.create_publisher(
            Float32,
            '/uav/relative_altitude',
            10
        )

        self.altitude = 0.0
        self.timer = self.create_timer(1.0, self.timer_callback)

        self.get_logger().info('Altitude publisher node started.')

    def timer_callback(self):
        msg = Float32()

        self.altitude += 0.1
        msg.data = self.altitude

        self.publisher_.publish(msg)

        self.get_logger().info(
            f'Publishing altitude: {msg.data:.2f} m'
        )


def main(args=None):
    rclpy.init(args=args)

    node = AltitudePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
