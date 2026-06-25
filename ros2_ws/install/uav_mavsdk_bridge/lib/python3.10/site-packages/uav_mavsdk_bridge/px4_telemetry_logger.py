import csv
import os
from pathlib import Path

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from std_msgs.msg import String


class PX4TelemetryLogger(Node):
    def __init__(self):
        super().__init__('px4_telemetry_logger')

        self.altitude = None
        self.roll = None
        self.pitch = None
        self.yaw = None
        self.flight_mode = None

        self.csv_path = Path.home() / 'uav-learning' / 'data' / 'month3' / 'ros2_px4_telemetry.csv'
        os.makedirs(self.csv_path.parent, exist_ok=True)

        self.csv_file = open(self.csv_path, mode='w', newline='')
        self.csv_writer = csv.writer(self.csv_file)

        self.csv_writer.writerow([
            'time_sec',
            'relative_altitude_m',
            'roll_deg',
            'pitch_deg',
            'yaw_deg',
            'flight_mode'
        ])

        self.create_subscription(
            Float32,
            '/px4/relative_altitude',
            self.altitude_callback,
            10
        )

        self.create_subscription(
            Float32,
            '/px4/roll',
            self.roll_callback,
            10
        )

        self.create_subscription(
            Float32,
            '/px4/pitch',
            self.pitch_callback,
            10
        )

        self.create_subscription(
            Float32,
            '/px4/yaw',
            self.yaw_callback,
            10
        )

        self.create_subscription(
            String,
            '/px4/flight_mode',
            self.flight_mode_callback,
            10
        )

        self.write_count = 0
        self.timer = self.create_timer(0.2, self.write_csv_row)

        self.get_logger().info(
            f'PX4 telemetry logger started. CSV path: {self.csv_path}'
        )

    def altitude_callback(self, msg):
        self.altitude = msg.data

    def roll_callback(self, msg):
        self.roll = msg.data

    def pitch_callback(self, msg):
        self.pitch = msg.data

    def yaw_callback(self, msg):
        self.yaw = msg.data

    def flight_mode_callback(self, msg):
        self.flight_mode = msg.data

    def write_csv_row(self):
        if self.altitude is None:
            return

        if self.roll is None or self.pitch is None or self.yaw is None:
            return

        now_sec = self.get_clock().now().nanoseconds / 1e9

        self.csv_writer.writerow([
            f'{now_sec:.3f}',
            f'{self.altitude:.3f}',
            f'{self.roll:.3f}',
            f'{self.pitch:.3f}',
            f'{self.yaw:.3f}',
            self.flight_mode if self.flight_mode is not None else ''
        ])

        self.csv_file.flush()

        self.write_count += 1

        if self.write_count % 10 == 0:
            self.get_logger().info(
                f'Wrote {self.write_count} rows to CSV. '
                f'alt={self.altitude:.2f} m, '
                f'roll={self.roll:.2f}, pitch={self.pitch:.2f}, yaw={self.yaw:.2f}'
            )

    def destroy_node(self):
        if hasattr(self, 'csv_file') and not self.csv_file.closed:
            self.csv_file.close()

        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = PX4TelemetryLogger()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
