import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from datetime import datetime, timedelta


class AutoMove(Node):

    def __init__(self):
        super().__init__('auto_move')

        # Publisher
        self.publisher = self.create_publisher(
            JointTrajectory,
            '/arm_controller/joint_trajectory',
            10
        )

        # ⏰ يتحرك بعد دقيقة من التشغيل
        self.target_time = datetime.now() + timedelta(minutes=1)

        self.executed = False

        # Check كل ثانية
        self.timer = self.create_timer(1.0, self.check_time)

        self.get_logger().info("⏰ Waiting 1 minute to execute motion...")

    def check_time(self):
        now = datetime.now()

        if now >= self.target_time and not self.executed:
            self.send_motion()
            self.executed = True

    def send_motion(self):

        msg = JointTrajectory()

        # أسماء joints (زي اللي عندك)
        msg.joint_names = [
            "link1_to_link2",
            "link2_to_link3",
            "link3_to_link4",
            "link4_to_link5",
            "link5_to_link6_flange",
            "gripper_controller"
        ]

        point = JointTrajectoryPoint()

        # ⚠️ الزوايا (radians)
        point.positions = [
            1.5,
            0.3,
            0.1,
            0.0,
            0.0,
            0.2
        ]

        point.time_from_start.sec = 3

        msg.points.append(point)

        self.publisher.publish(msg)

        self.get_logger().info("🚀 Motion executed!")


def main(args=None):
    rclpy.init(args=args)
    node = AutoMove()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
