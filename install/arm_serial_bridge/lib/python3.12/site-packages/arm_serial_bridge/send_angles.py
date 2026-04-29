import rclpy
from rclpy.node import Node
import serial
import time

class SendAngles(Node):

    def __init__(self):
        super().__init__('send_angles')

        # 🔌 Serial
        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        time.sleep(2)

        # ⏱️ ابعت بعد 3 ثواني
        self.timer = self.create_timer(3.0, self.send_once)
        self.sent = False

        self.get_logger().info("🚀 Ready to send angles")

    def send_once(self):
        if self.sent:
            return

        # 🎯 الزوايا (غيّرها براحتك)
        angles = [0, 0, 0, 0, 0, 0]

        data = ",".join(map(str, angles)) + "\n"

        self.ser.write(data.encode())

        self.get_logger().info(f"📡 Sent: {data.strip()}")

        self.sent = True


def main():
    rclpy.init()
    node = SendAngles()
    rclpy.spin(node)
    rclpy.shutdown()
