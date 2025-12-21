
import os
import cv2
import mediapipe as mp
import numpy as np
import math
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.utils.camera_utils import CameraHandler

class GestureDetection:
    # detects hand gesture using media pie and open cv
    def __init__(self,detection_confidence=0.7, tracking_confidence=0.5):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.current_gesture = "none"
        self.WRIST = 0
        self.THUMB_TIP = 4
        self.INDEX_TIP = 8
        self.MIDDLE_TIP = 12
        self.RING_TIP = 16
        self.PINKY_TIP = 20
    
    def get_hands(self,frame,draw=True):
        if frame is not None:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)
            if results and results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
            return frame,results

        else:
            print("no frame")

    def get_landmarks(self, hand_landmarks, frame_width, frame_height):
        landmarks = []
        
        for id, landmark in enumerate(hand_landmarks.landmark):
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            landmarks.append([id, x, y])
        
        return landmarks
    
if __name__ == "__main__":
   
    
    print("=== Hand Detection Test ===")
    print("Press 'q' to quit")
    
    # Initialize camera and detector  
    cam = CameraHandler()
    detector = GestureDetection()    
    frame_width, frame_height = cam.get_frame_dimensions()

    
    while True:
        success, frame = cam.read_frame()
        
        if success:
            # Detect hands and draw landmarks
            frame, results = detector.get_hands(frame, draw=True)
            
            # If hand detected, print landmark count
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = detector.get_landmarks(
                        hand_landmarks, 
                        frame_width, 
                        frame_height
                    )
                    
                    # Display info on frame
                    cv2.putText(
                        frame, 
                        f"Hand Detected! {len(landmarks)} landmarks", 
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0, 255, 0),
                        2
                    )
            
            # Display frame
            cam.display_frame(frame, "Hand Detection Test")
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cam.release_camera()
    print("Test completed!")