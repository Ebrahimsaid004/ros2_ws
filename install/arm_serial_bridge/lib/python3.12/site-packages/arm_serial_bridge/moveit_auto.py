import rclpy
from rclpy.node import Node
from datetime import datetime, timedelta

class MoveItAuto(Node):

    def __init__(self):
        super().__init__('moveit_auto')

        # بعد 20 ثانية
        self.target_time = datetime.now() + timedelta(seconds=20)

        self.executed = False
        self.timer = self.create_timer(1.0, self.check_time)

        self.get_logger().info("⏰ Waiting...")

    def check_time(self):
        now = datetime.now()

        if now >= self.target_time and not self.executed:
            self.execute_motion()
            self.executed = True

    def execute_motion(self):
        self.get_logger().info("🚀 Trigger movement now!")

        # هنا هنستخدم system call يشغل MoveIt execution
        import os
        os.system("ros2 topic pub -1 /arm_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory \"{joint_names: ['link1_to_link2','link2_to_link3','link3_to_link4','link4_to_link5','link5_to_link6_flange','gripper_controller'], points: [{positions: [1.5,0.3,0.1,0.0,0.0,0.2], time_from_start: {sec: 2}}]}\"")


def main():
    rclpy.init()
    node = MoveItAuto()
    rclpy.spin(node)
    rclpy.shutdown()
