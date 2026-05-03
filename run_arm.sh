#!/bin/bash

# مهم جدًا: source للـ ROS2 Jazzy

cd ~/ros2_ws || exit
colcon build
source /opt/ros/jazzy/setup.bash

source install/setup.bash

ros2 run arm_serial_bridge send_angles&
PID=$!
sleep 5

kill -2 $PID
