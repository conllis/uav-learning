import math

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32


class AttitudePublisher(Node):
    def __init__(self):
        super().__init__('attitude_publisher')

        self.roll_publisher = self.create_publisher(
            Float32,
            '/uav/roll',
            10
        )

        self.pitch_publisher = self.create_publisher(
            Float32,
            '/uav/pitch',
            10
        )

        self.yaw_publisher = self.create_publisher(
            Float32,
            '/uav/yaw',
            10
        )

        self.time_sec = 0.0
        self.timer = self.create_timer(0.5, self.timer_callback)

        self.get_logger().info('Attitude publisher node started.')

    def timer_callback(self):
        self.time_sec += 0.5

        roll = 10.0 * math.sin(self.time_sec)
        pitch = 5.0 * math.sin(0.5 * self.time_sec)
        yaw = (self.time_sec * 15.0) % 360.0

        roll_msg = Float32()
        pitch_msg = Float32()
        yaw_msg = Float32()

        roll_msg.data = roll
        pitch_msg.data = pitch
        yaw_msg.data = yaw

        self.roll_publisher.publish(roll_msg)
        self.pitch_publisher.publish(pitch_msg)
        self.yaw_publisher.publish(yaw_msg)

        self.get_logger().info(
            f'Publishing attitude: roll={roll:.2f} deg, '
            f'pitch={pitch:.2f} deg, yaw={yaw:.2f} deg'
        )


def main(args=None):
    rclpy.init(args=args)

    node = AttitudePublisher()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
