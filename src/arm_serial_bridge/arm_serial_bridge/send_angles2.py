import rclpy
from rclpy.node import Node
import serial
import time

class SerialSender(Node):

    def __init__(self):
        super().__init__('serial_sender')

        self.ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
        time.sleep(2)

        self.get_logger().info("🚀 Serial Ready")

    def send(self, angles):
        data = ",".join(map(str, angles)) + "\n"
        self.ser.write(data.encode())
        self.get_logger().info(f"Sent: {data.strip()}")


def main():
    rclpy.init()
    node = SerialSender()

    # 🧪 جرّب كذا حركة ورا بعض
    time.sleep(2)
    node.send([100,100,100,100,100,100])

    time.sleep(6)
    node.send([10,10,10,10,10,10])
    
    time.sleep(6)
    node.send([0,0,0,0,0,0])

    rclpy.spin(node)
