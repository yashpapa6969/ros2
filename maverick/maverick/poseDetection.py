import cv2
import mediapipe as mp
import rclpy
from rclpy.node import Node
from custom_interfaces.msg import PoseLandmark
from geometry_msgs.msg import Point

class PoseDetectionPublisher(Node):
    def __init__(self):
        super().__init__('pose_detection_publisher')
        self.publisher_ = self.create_publisher(PoseLandmark, 'pose_landmarks', 10)
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(static_image_mode=False, model_complexity=2, smooth_landmarks=True,
                                      enable_segmentation=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.drawing_utils = mp.solutions.drawing_utils

    def run_pose_detection(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.get_logger().error("Cannot open webcam")
            return

        try:
            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    self.get_logger().warn("Ignoring empty camera frame.")
                    continue

                image = self.process_image(image)
                cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
                if cv2.waitKey(5) & 0xFF == 27:  # Exit loop if 'ESC' is pressed
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

    def process_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        if results.pose_landmarks:
            self.draw_landmarks(image, results.pose_landmarks)
            self.plot_landmarks_and_publish(results.pose_world_landmarks)
        return image

    def draw_landmarks(self, image, landmarks):
        self.drawing_utils.draw_landmarks(
            image, landmarks, self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.drawing_utils.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
            connection_drawing_spec=self.drawing_utils.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

    def plot_landmarks_and_publish(self, landmarks):
        landmarks_labels = {
            11: "left_shoulder", 12: "right_shoulder",
            13: "left_elbow", 14: "right_elbow",
            15: "left_wrist", 16: "right_wrist",
            23: "left_hip", 24: "right_hip",
        }
        pose_landmark_msg = PoseLandmark()
        for idx, landmark in enumerate(landmarks.landmark):
            if idx in landmarks_labels:
                label = landmarks_labels[idx]
                pose_landmark_msg.label.append(label)
                pose_landmark_msg.point.append(Point(x=landmark.x, y=landmark.y, z=landmark.z))

        self.publisher_.publish(pose_landmark_msg)

def main(args=None):
    rclpy.init(args=args)
    node = PoseDetectionPublisher()
    node.run_pose_detection()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
