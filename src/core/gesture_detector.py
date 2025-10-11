
import mediapipe as mp
import numpy as np
import math

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

