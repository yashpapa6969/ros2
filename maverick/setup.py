import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'maverick'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        # Add resources directories
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'meshes', 'stl'), glob('meshes/stl/*')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jaeho',
    maintainer_email='jaeho.cho@cooper.edu',
    description='maverick',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'poseDetection = maverick.poseDetection:main',
            'poseDisplay = maverick.poseDisplay:main',
            'shoulderAdduction = maverick.shoulderAdduction:main',
            'shoulderFlexion = maverick.shoulderFlexion:main',
            'elbowFlexion = maverick.elbowFlexion:main',
            'jointStatePublisher = maverick.jointStatePublisher:main',
            'displayJointStates = maverick.displayJointStates:main',
        ],
    },
)
