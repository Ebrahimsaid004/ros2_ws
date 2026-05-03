from setuptools import setup

package_name = 'arm_serial_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ibrahim',
    maintainer_email='ibrahim@example.com',
    description='ROS2 Serial Bridge for Robot Arm',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'joint_to_serial = arm_serial_bridge.joint_to_serial:main',
            'send_angles = arm_serial_bridge.send_angles:main',
            'send_angles2 = arm_serial_bridge.send_angles2:main',
        ],
    },
)
