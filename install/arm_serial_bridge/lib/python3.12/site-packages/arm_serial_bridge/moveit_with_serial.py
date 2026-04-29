import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
import serial
import time
import math
import os

class MoveItSerial(Node):

    def __init__(self):
        super().__init__('moveit_serial')

        # 🔌 Serial
        self.ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        time.sleep(2)

        self.joint_names = [
            "link1_to_link2",
            "link2_to_link3",
            "link3_to_link4",
            "link4_to_link5",
            "link5_to_link6_flange",
            "gripper_controller"
        ]

        self.subscription = self.create_subscription(
            JointState,
            '/joint_states',
            self.callback,
            10
        )

        self.timer = self.create_timer(5.0, self.send_motion)
        self.sent = False

        self.get_logger().info("🚀 MoveIt + Serial Node Running")

    def send_motion(self):
        if self.sent:
            return

        self.get_logger().info("📤 Sending goal to MoveIt")

        os.system("ros2 topic pub -1 /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \"{joint_names: ['link1_to_link2','link2_to_link3','link3_to_link4','link4_to_link5','link5_to_link6_flange','gripper_controller'], points: [{positions: [1.5,0.3,0.1,0.0,0.0,0.2], time_from_start: {sec: 2}}]}\"")

        self.sent = True

    def callback(self, msg):
        angles = []

        for name in self.joint_names:
            if name in msg.name:
                idx = msg.name.index(name)
                rad = msg.position[idx]

                deg = int(rad * 180 / math.pi)
                deg = max(0, min(180, deg))

                angles.append(deg)

        if len(angles) == 6:
            data = ",".join(map(str, angles)) + "\n"
            self.ser.write(data.encode())

            self.get_logger().info(f"📡 Sent: {data.strip()}")

def main():
    rclpy.init()
    node = MoveItSerial()
    rclpy.spin(node)
    rclpy.shutdown()
