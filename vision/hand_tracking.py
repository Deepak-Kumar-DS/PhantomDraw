"""
PhantomDraw AI
Advanced Hand Tracking Module

Features:
- Detects up to two hands.
- Tracks 21 hand landmarks.
- Identifies Left and Right hands.
- Provides hand positions.
- Supports gesture interaction.
"""

import cv2
import mediapipe as mp


class HandTracker:

    def __init__(
        self,
        max_hands=2,
        detection_confidence=0.7,
        tracking_confidence=0.7
    ):

        self.mp_hands = mp.solutions.hands

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.mp_draw = mp.solutions.drawing_utils

        self.results = None

    def process_frame(self, frame):
        """Detect hands in a camera frame."""

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        self.results = self.hands.process(rgb_frame)

        return self.results

    def draw_landmarks(self, frame):
        """Draw detected hand landmarks."""

        if self.results and self.results.multi_hand_landmarks:

            for hand_landmarks in self.results.multi_hand_landmarks:

                self.mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return frame

    def get_hand_count(self):
        """Return detected hand count."""

        if self.results and self.results.multi_hand_landmarks:

            return len(self.results.multi_hand_landmarks)

        return 0

    def get_landmarks(self, hand_index=0):
        """Return landmarks of a specific hand."""

        if not self.results:
            return None

        hands = self.results.multi_hand_landmarks

        if hands and 0 <= hand_index < len(hands):

            return hands[hand_index]

        return None

    def get_all_landmarks(self):
        """Return landmarks of all detected hands."""

        if self.results and self.results.multi_hand_landmarks:

            return self.results.multi_hand_landmarks

        return []

    def get_handedness(self):
        """
        Return Left/Right classification
        for every detected hand.
        """

        if self.results and self.results.multi_handedness:

            return self.results.multi_handedness

        return []

    def get_hand_label(self, hand_index=0):
        """Return Left or Right label."""

        handedness = self.get_handedness()

        if 0 <= hand_index < len(handedness):

            try:

                return handedness[
                    hand_index
                ].classification[0].label

            except (AttributeError, IndexError, TypeError):

                return "Unknown"

        return "Unknown"

    def get_finger_position(self, hand_index=0, finger_id=8):
        """Return normalized landmark position."""

        landmarks = self.get_landmarks(hand_index)

        if landmarks is None:
            return None

        landmark = landmarks.landmark[finger_id]

        return landmark.x, landmark.y

    def close(self):
        """Release MediaPipe resources."""

        self.hands.close()

        print("Hand tracker stopped.")