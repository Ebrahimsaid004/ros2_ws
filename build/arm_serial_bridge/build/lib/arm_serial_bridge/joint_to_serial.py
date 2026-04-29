import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import serial
import math

class JointToSerial(Node):

    def __init__(self):
        super().__init__('joint_to_serial')

        # ⚠️ عدّل البورت حسب جهازك
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

        # 👇 الـ 6 joints الحقيقيين عندك (من /joint_states)
        self.joint_map = {
            "link1_to_link2": 0,
            "link2_to_link3": 1,
            "link3_to_link4": 2,
            "link4_to_link5": 3,
            "link5_to_link6_flange": 4,
            "gripper_controller": 5
        }

        self.angles = [90] * 6  # default safe position

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.callback,
            10
        )

        self.get_logger().info("🚀 6DOF ROS2 → Arduino Bridge Running")

    def callback(self, msg):

        # update only relevant joints
        for i, name in enumerate(msg.name):

            if name in self.joint_map:

                idx = self.joint_map[name]

                # rad → deg
                deg = math.degrees(msg.position[i])

                # limit servo range
                deg = max(0, min(180, deg))

                self.angles[idx] = int(deg)

        # send to Arduino
        data = "{},{},{},{},{},{}\n".format(*self.angles)

        self.ser.write(data.encode())

        self.get_logger().info(f"Sent: {data.strip()}")


def main(args=None):
    rclpy.init(args=args)
    node = JointToSerial()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
