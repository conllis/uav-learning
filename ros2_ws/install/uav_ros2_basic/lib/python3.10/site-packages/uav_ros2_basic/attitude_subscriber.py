import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class AttitudeSubscriber(Node):
    def __init__(self):
        super().__init__('attitude_subscriber')

        self.roll = None
        self.pitch = None
        self.yaw = None

        self.roll_subscription = self.create_subscription(
            Float32,
            '/uav/roll',
            self.roll_callback,
            10
        )

        self.pitch_subscription = self.create_subscription(
            Float32,
            '/uav/pitch',
            self.pitch_callback,
            10
        )

        self.yaw_subscription = self.create_subscription(
            Float32,
            '/uav/yaw',
            self.yaw_callback,
            10
        )

        self.get_logger().info('Attitude subscriber node started.')

    def roll_callback(self, msg):
        self.roll = msg.data
        self.print_attitude()

    def pitch_callback(self, msg):
        self.pitch = msg.data
        self.print_attitude()

    def yaw_callback(self, msg):
        self.yaw = msg.data
        self.print_attitude()

    def print_attitude(self):
        if self.roll is None or self.pitch is None or self.yaw is None:
            return

        self.get_logger().info(
            f'Received attitude: roll={self.roll:.2f} deg, '
            f'pitch={self.pitch:.2f} deg, yaw={self.yaw:.2f} deg'
        )


def main(args=None):
    rclpy.init(args=args)

    node = AttitudeSubscriber()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
