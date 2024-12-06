import numpy as np
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState
from std_msgs.msg import Header

class JointStatePublisher(Node):

    def __init__(self):
        super().__init__('joint_state_publisher')
        
        # Define joint names for each side
        self.sides = ['left', 'right']
        self.joint_types = ['shoulder_flexion', 'shoulder_adduction', 'elbow_flexion']
        self.joint_names = [f'{side}_{joint_type}' for side in self.sides for joint_type in self.joint_types]
        
        # Initialize a dictionary to keep track of the latest joint angles with default 0.0
        self.joint_angles = {joint_name: 0.0 for joint_name in self.joint_names}
        
        # Create subscriptions dynamically
        for joint_name in self.joint_names:
            self.create_subscription(Float64, joint_name, self.create_handler(joint_name), 10)
        
        self.joint_state_publisher = self.create_publisher(JointState, 'joint_states', 10)

    def create_handler(self, joint_name):
        def handler(msg):
            self.joint_angles[joint_name] = msg.data
            self.publish_joint_state()
        return handler

    def publish_joint_state(self):
        joint_state_msg = JointState()
        joint_state_msg.header = Header()
        joint_state_msg.header.stamp = self.get_clock().now().to_msg()
        
        robot_joint_names = []
        joint_positions = []
        
        for side in self.sides:
            robot_joint_names.extend([
                f'{side}_joint1', f'{side}_joint2', f'{side}_joint3',
                f'{side}_joint4', f'{side}_gripper', f'{side}_gripper_sub'
            ])
            
            if side == 'left':
                shoulder_flexion_angle = self.joint_angles[f'{side}_shoulder_flexion']
            else:
                shoulder_flexion_angle = -self.joint_angles[f'{side}_shoulder_flexion']
            
            joint_positions.extend([
                shoulder_flexion_angle,
                -self.joint_angles[f'{side}_shoulder_adduction'] + np.pi / 2,
                -self.joint_angles[f'{side}_elbow_flexion'] + np.pi / 2,
                0.0, 0.0, 0.0  # Placeholder for other joint values not computed
            ])
        
        joint_state_msg.name = robot_joint_names
        joint_state_msg.position = joint_positions
        joint_state_msg.velocity = []
        joint_state_msg.effort = []

        self.joint_state_publisher.publish(joint_state_msg)

def main(args=None):
    rclpy.init(args=args)
    joint_state_publisher = JointStatePublisher()
    rclpy.spin(joint_state_publisher)
    joint_state_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
