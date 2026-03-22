"""
Hand Gesture Mouse Control - Main Application
Integrates gesture detection with mouse control for hands-free computer interaction.
"""

import cv2
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src.core.gesture_detector import GestureDetection
from src.core.mouse_controller import MouseController
from src.utils.camera_utils import CameraHandler


class HandGestureMouseControl:
    """Main application class that integrates gesture detection with mouse control."""
    
    def __init__(self, camera_id=0, frame_width=640, frame_height=480):
        """Initialize the application components."""
        print("\n📋 Initializing components...")
        
        # Initialize camera
        try:
            self.camera = CameraHandler(camera_id, frame_width, frame_height)
            self.frame_width, self.frame_height = self.camera.get_frame_dimensions()
            print(f"✅ Camera initialized: {self.frame_width}x{self.frame_height}")
        except Exception as e:
            print(f"❌ Camera initialization failed: {e}")
            sys.exit(1)
        
        # Initialize gesture detector
        try:
            self.gesture_detector = GestureDetection(
                detection_confidence=0.7,
                tracking_confidence=0.5
            )
            print("✅ Gesture detector initialized")
        except Exception as e:
            print(f"❌ Gesture detector initialization failed: {e}")
            self.camera.release_camera()
            sys.exit(1)
        
        # Initialize mouse controller
        try:
            self.mouse_controller = MouseController()
            print("✅ Mouse controller initialized")
        except Exception as e:
            print(f"❌ Mouse controller initialization failed: {e}")
            self.camera.release_camera()
            sys.exit(1)
        
        # Previous gesture state for drag handling
        self.previous_gesture = "none"
        
        print("\n" + "-"*60)
        print("🎮 GESTURE CONTROLS:")
        print("-"*60)
        print("  👆 POINT    - Move cursor (extend index finger)")
        print("  🤏 PINCH    - Left click (thumb + index)")
        print("  ✌️  V-SIGN   - Right click (thumb + middle)")
        print("  ✊ FIST     - Drag (close all fingers)")
        print("  ✋ OTHER    - No action")
        print("\n  Press 'q' to quit")
        print("  Move mouse to TOP-LEFT corner for emergency stop")
        print("="*60 + "\n")
    
    def process_gesture(self, gesture, landmarks):
        """Process detected gesture and perform corresponding mouse action."""
        if gesture == "point":
            # Move cursor using index finger position
            index_x, index_y = self.gesture_detector.get_finger_position(landmarks, "index")
            if index_x is not None and index_y is not None:
                # Map camera coordinates to screen coordinates
                screen_x, screen_y = self.mouse_controller.map_coordinates(
                    index_x, index_y,
                    self.frame_width, self.frame_height,
                    padding=50,  # Dead zone from edges
                    flip=True     # Mirror effect
                )
                self.mouse_controller.move_cursor(screen_x, screen_y)
                
                # Stop dragging if we were dragging
                if self.previous_gesture == "fist":
                    self.mouse_controller.drag_end()
        
        elif gesture == "pinch":
            # Left click
            if self.previous_gesture != "pinch":  # Only click once per gesture
                self.mouse_controller.left_click()
        
        elif gesture == "right_click":
            # Right click
            if self.previous_gesture != "right_click":  # Only click once per gesture
                self.mouse_controller.right_click()
        
        elif gesture == "fist":
            # Start or continue dragging
            if self.previous_gesture != "fist":
                # Start drag at current position
                index_x, index_y = self.gesture_detector.get_finger_position(landmarks, "index")
                if index_x is not None and index_y is not None:
                    screen_x, screen_y = self.mouse_controller.map_coordinates(
                        index_x, index_y,
                        self.frame_width, self.frame_height,
                        padding=50,
                        flip=True
                    )
                    self.mouse_controller.move_cursor(screen_x, screen_y)
                    self.mouse_controller.start_drag()
            else:
                # Continue dragging - move cursor while dragging
                index_x, index_y = self.gesture_detector.get_finger_position(landmarks, "index")
                if index_x is not None and index_y is not None:
                    screen_x, screen_y = self.mouse_controller.map_coordinates(
                        index_x, index_y,
                        self.frame_width, self.frame_height,
                        padding=50,
                        flip=True
                    )
                    self.mouse_controller.move_cursor(screen_x, screen_y)
        
        elif gesture == "none":
            # Stop dragging if we were dragging
            if self.previous_gesture == "fist":
                self.mouse_controller.drag_end()
        
        # Update previous gesture
        self.previous_gesture = gesture
    
    def draw_ui(self, frame, gesture, finger_count, index_x, index_y):
        """Draw UI overlay on the frame."""
        frame_height, frame_width = frame.shape[:2]
        
        # Top-left: Current gesture info
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (300, 120), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.6, frame, 0.4, 0, frame)
        
        # Gesture display
        gesture_text = f"GESTURE: {gesture.upper()}"
        color = (0, 255, 0) if gesture != "none" else (200, 200, 200)
        cv2.putText(
            frame, gesture_text, (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2
        )
        
        # Finger count
        cv2.putText(
            frame, f"Fingers: {finger_count}", (20, 60),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1
        )
        
        # Index finger position
        if index_x is not None and index_y is not None:
            cv2.putText(
                frame, f"Index: ({index_x}, {index_y})", (20, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1
            )
        
        # Instructions
        cv2.putText(
            frame, "Press 'q' to quit", (20, 110),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (200, 200, 200), 1
        )
        
        # Bottom-left: Gesture controls
        controls_y_start = frame_height - 150
        controls_x = 10
        overlay_bottom = frame.copy()
        cv2.rectangle(overlay_bottom, (controls_x, controls_y_start), (350, frame_height - 10), (0, 0, 0), -1)
        cv2.addWeighted(overlay_bottom, 0.7, frame, 0.3, 0, frame)
        
        # Gesture controls list
        controls = [
            ("POINT", "Moves cursor", (0, 255, 255)),
            ("PINCH", "Left click", (0, 255, 0)),
            ("V-SIGN", "Right click", (255, 0, 0)),
            ("FIST", "Drag operation", (255, 165, 0)),
            ("OTHER", "No action", (200, 200, 200))
        ]
        
        y_offset = controls_y_start + 25
        for control_name, control_action, control_color in controls:
            control_text = f"{control_name:8} -> {control_action}"
            cv2.putText(
                frame, control_text, (controls_x + 10, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, control_color, 1
            )
            y_offset += 22
        
        # Draw circle at index finger if available
        if index_x is not None and index_y is not None:
            cv2.circle(frame, (index_x, index_y), 10, (0, 255, 255), 2)
    
    def run(self):
        """Main application loop."""
        print("🚀 Starting application...\n")
        
        frame_count = 0
        
        try:
            while True:
                # Read frame from camera
                success, frame = self.camera.read_frame()
                
                if not success or frame is None:
                    print("⚠️  Failed to read frame")
                    break
                
                frame_count += 1
                
                # Detect hands and get landmarks
                frame, results = self.gesture_detector.get_hands(frame, draw=True)
                
                current_gesture = "none"
                finger_count = 0
                index_x, index_y = None, None
                
                if results and results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # Get landmarks
                        landmarks = self.gesture_detector.get_landmarks(
                            hand_landmarks,
                            self.frame_width,
                            self.frame_height
                        )
                        
                        # Validate landmarks
                        if landmarks is None or len(landmarks) < 21:
                            continue
                        
                        # Count fingers and detect gesture
                        fingers_up, finger_count = self.gesture_detector.count_fingers_up(landmarks)
                        current_gesture = self.gesture_detector.detect_gesture(landmarks, fingers_up)
                        
                        # Get index finger position
                        index_x, index_y = self.gesture_detector.get_finger_position(landmarks, "index")
                        
                        # Process gesture and control mouse
                        self.process_gesture(current_gesture, landmarks)
                
                else:
                    # No hand detected - stop dragging if we were dragging
                    if self.previous_gesture == "fist":
                        self.mouse_controller.drag_end()
                    self.previous_gesture = "none"
                
                # Draw UI overlay
                self.draw_ui(frame, current_gesture, finger_count, index_x, index_y)
                
                # Display frame
                self.camera.display_frame(frame, "Hand Gesture Mouse Control - Press 'q' to Quit")
                
                # Check for quit
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\n👋 Quitting application...")
                    break
        
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrupted by user (Ctrl+C)")
        except Exception as e:
            print(f"\n❌ Error occurred: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Cleanup
            if self.previous_gesture == "fist":
                self.mouse_controller.drag_end()
            self.camera.release_camera()
            print(f"\n✅ Application closed. Processed {frame_count} frames.")
            print("="*60 + "\n")


def main():
    """Entry point for the application."""
    try:
        app = HandGestureMouseControl(
            camera_id=0,
            frame_width=640,
            frame_height=480
        )
        app.run()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
