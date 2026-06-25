from setuptools import find_packages, setup

package_name = 'uav_mavsdk_bridge'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zzz',
    maintainer_email='578427822@qq.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        	'px4_telemetry_bridge = uav_mavsdk_bridge.px4_telemetry_bridge:main',
        	'px4_telemetry_logger = uav_mavsdk_bridge.px4_telemetry_logger:main',
        	'px4_action_command_node = uav_mavsdk_bridge.px4_action_command_node:main',
        ],
    },
)
