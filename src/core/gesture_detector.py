
import os
import cv2
import mediapipe as mp
import numpy as np
import math
import sys

from pyautogui import position
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
    
    def get_distance(self, p1, p2):
        # Calculate Euclidean distance between two points
        if len(p1) ==3 and len(p2) ==3:
            x1, y1 = p1[1], p1[2]
            x2, y2 = p2[1], p2[2]
        else:
            x1, y1 = p1[0], p1[1]
            x2, y2 = p2[0], p2[1]
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return distance
    
    def count_fingers_up(self, landmarks):
        # Count how many fingers are up based on landmarks
        # Returns:
        # fingers_up: List of 5 booleans [thumb, index, middle, ring, pinky]
        # count: Integer count of fingers that are up
        fingers_up = []
        # Thumb
        if landmarks[self.THUMB_TIP][1] > landmarks[self.THUMB_TIP - 1][1]:
            fingers_up.append(True)
        else:
            fingers_up.append(False)
        # Other four fingers
        for tip_id in [self.INDEX_TIP, self.MIDDLE_TIP, self.RING_TIP, self.PINKY_TIP]:
            if landmarks[tip_id][2] < landmarks[tip_id - 2][2]:
                fingers_up.append(True)
            else:
                fingers_up.append(False)
        count = fingers_up.count(True)
        return fingers_up, count
    
    def detect_gesture(self, landmarks, fingers_up):
        thumb_tip = landmarks[self.THUMB_TIP]
        index_tip = landmarks[self.INDEX_TIP]
        middle_tip = landmarks[self.MIDDLE_TIP]
        ring_tip = landmarks[self.RING_TIP]
        thumb_index_distance = self.get_distance(thumb_tip, index_tip)
        thumb_middle_distance = self.get_distance(thumb_tip, middle_tip)
        
        # Count fingers
        finger_count = fingers_up.count(True)
        
        # Gesture detection logic (order matters!)
        
        # 1. PINCH (Left Click) - Thumb and index finger close together
        if thumb_index_distance < 40:  # 40 pixels threshold
            return "pinch"
        
        # 2. RIGHT CLICK - Thumb and middle finger close together
        elif thumb_middle_distance < 40:
            return "right_click"
        
        # 3. POINT (Move cursor) - Only index finger is up
        elif finger_count == 1 and fingers_up[1]:  # fingers_up[1] is index finger
            return "point"
        
        # 4. FIST (Drag) - No fingers up (all closed)
        elif finger_count == 0:
            return "fist"
        
        # 5. NONE - Any other hand position
        else:
            return "none"
    
    def get_finger_position(self, landmarks, finger_name="index"):
    # Get the position of a specific finger tip

    # Validate landmarks
        if landmarks is None or len(landmarks) < 21:
            print(f"⚠️ Warning: Invalid landmarks (expected 21, got {len(landmarks) if landmarks else 0})")
            return None, None
        
        # Map finger names to landmark IDs
        finger_map = {
            "thumb": self.THUMB_TIP,      # 4
            "index": self.INDEX_TIP,      # 8
            "middle": self.MIDDLE_TIP,    # 12
            "ring": self.RING_TIP,        # 16
            "pinky": self.PINKY_TIP       # 20
        }
        
        # Get the landmark ID for this finger (default to index if not found)
        finger_id = finger_map.get(finger_name.lower(), self.INDEX_TIP)
        
        # Verify the finger_id is within valid range
        if finger_id < 0 or finger_id >= len(landmarks):
            print(f"⚠️ Warning: Invalid finger_id {finger_id}")
            return None, None
        
        # Verify landmark has correct format [id, x, y]
        if len(landmarks[finger_id]) < 3:
            print(f"⚠️ Warning: Landmark {finger_id} has invalid format")
            return None, None
        
        # Return x, y coordinates
        x = landmarks[finger_id][1]
        y = landmarks[finger_id][2]
        
        return x, y
if __name__ == "__main__":
    print("\n" + "="*60)
    print("       GESTURE RECOGNITION TEST")
    print("="*60)
    print("\n📋 Test these gestures:")
    print("   👆 POINT    - Extend only index finger")
    print("   🤏 PINCH    - Touch thumb and index finger")
    print("   ✌️  V-SIGN   - Touch thumb and middle finger")
    print("   ✊ FIST     - Close all fingers")
    print("   ✋ OTHER    - Any other position")
    print("\n   Press 'q' to quit\n")
    print("="*60 + "\n")
    
    try:
        cam = CameraHandler()
        detector = GestureDetection()
        frame_width, frame_height = cam.get_frame_dimensions()
        
        print("✅ Ready! Try different hand gestures...\n")
        
        gesture_counts = {
            "point": 0,
            "pinch": 0,
            "right_click": 0,
            "fist": 0,
            "none": 0
        }
        
        frame_count = 0
        
        while True:
            success, frame = cam.read_frame()
            
            if not success:
                break
            
            frame_count += 1
            frame, results = detector.get_hands(frame, draw=True)
            
            if frame is None:
                continue
            
            current_gesture = "none"
            finger_count = 0
            
            if results and results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    landmarks = detector.get_landmarks(
                        hand_landmarks, frame_width, frame_height
                    )
                    
                    # Validate landmarks before using them
                    if landmarks is None or len(landmarks) < 21:
                        print("⚠️ Warning: Invalid landmarks detected")
                        continue
                    
                    # Count fingers and detect gesture
                    fingers_up, finger_count = detector.count_fingers_up(landmarks)
                    current_gesture = detector.detect_gesture(landmarks, fingers_up)
                    
                    # Update statistics
                    if current_gesture in gesture_counts:
                        gesture_counts[current_gesture] += 1
                    
                    # Get index finger position (with error handling)
                    index_x, index_y = detector.get_finger_position(landmarks, "index")
                    
                    # Display gesture info
                    gesture_text = f"GESTURE: {current_gesture.upper()}"
                    color = (0, 255, 0) if current_gesture != "none" else (200, 200, 200)
                    
                    cv2.putText(
                        frame, gesture_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2
                    )
                    
                    # Display finger count
                    cv2.putText(
                        frame, f"Fingers up: {finger_count}", (10, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1
                    )
                    
                    # Display index finger position (with None check)
                    if index_x is not None and index_y is not None:
                        cv2.putText(
                            frame, f"Index: ({index_x}, {index_y})", (10, 85),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1
                        )
                        
                        # Draw circle at index finger tip
                        cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), -1)
                    else:
                        cv2.putText(
                            frame, "Index: N/A", (10, 85),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1
                        )
            else:
                cv2.putText(
                    frame, "No hand detected", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2
                )
            
            cam.display_frame(frame, "Gesture Test - Press 'q' to Quit")
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        # Print statistics
        print("\n" + "="*60)
        print("       GESTURE TEST RESULTS")
        print("="*60)
        print(f"\nTotal frames: {frame_count}")
        print("\nGesture detections:")
        for gesture, count in gesture_counts.items():
            if count > 0:
                percentage = (count / frame_count) * 100
                print(f"   {gesture:12} - {count:4} times ({percentage:5.1f}%)")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        cam.release_camera()
        print("✅ Test completed!\n")