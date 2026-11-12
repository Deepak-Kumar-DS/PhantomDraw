"""
PhantomDraw AI
Gesture Detection Engine

Gestures:
- DRAW: Index finger raised
- OPEN_PALM: All fingers raised
- THUMB_UP: Thumb raised, other fingers folded
- FIST: All fingers folded
- SELECT: Index and middle fingers raised
"""

class GestureDetector:

    def __init__(self):
        self.finger_names = [
            "THUMB",
            "INDEX",
            "MIDDLE",
            "RING",
            "PINKY"
        ]

    def get_finger_states(self, landmarks):

        points = landmarks.landmark

        fingers = {}

        # Thumb: vertical upward detection
        fingers["THUMB"] = (
            points[4].y < points[3].y
        )

        # Other fingers
        finger_pairs = {
            "INDEX": (8, 6),
            "MIDDLE": (12, 10),
            "RING": (16, 14),
            "PINKY": (20, 18)
        }

        for finger, (tip, joint) in finger_pairs.items():

            fingers[finger] = (
                points[tip].y < points[joint].y
            )

        return fingers

    def detect_gesture(self, landmarks):

        fingers = self.get_finger_states(landmarks)

        thumb = fingers["THUMB"]
        index = fingers["INDEX"]
        middle = fingers["MIDDLE"]
        ring = fingers["RING"]
        pinky = fingers["PINKY"]

        # Thumb Up: UI selection gesture
        if thumb and not index and not middle and not ring and not pinky:
            return "THUMB_UP"

        # Open palm
        if index and middle and ring and pinky:
            return "OPEN_PALM"

        # Drawing gesture
        if index and not middle and not ring and not pinky:
            return "DRAW"

        # Select gesture
        if index and middle and not ring and not pinky:
            return "SELECT"

        # Fist
        if not thumb and not index and not middle and not ring and not pinky:
            return "FIST"

        return "UNKNOWN"

    def get_gesture_label(self, gesture):

        labels = {
            "DRAW": "Drawing",
            "OPEN_PALM": "Open Palm",
            "THUMB_UP": "Thumb Up - Select",
            "SELECT": "Select",
            "FIST": "Fist",
            "UNKNOWN": "Unknown"
        }

        return labels.get(gesture, "Unknown")