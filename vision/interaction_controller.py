
"""
PhantomDraw AI
Advanced Interaction Controller

Features:
- Automatic Hand Detection
- Single Hand Mode
- Two Hand Mode
- Left / Right Hand Recognition
- Automatic Drawing Hand Assignment
- Automatic Control Hand Assignment
- Digital Tap Detection
- Pinch Detection
- Tap Hold Detection
- Accidental Tap Prevention
"""

import math
import time


class InteractionController:

    def __init__(self):

        # =====================================
        # HAND MODE
        # =====================================

        self.mode = "NO_HAND"

        self.hand_count = 0

        self.is_drawing_allowed = False

        # =====================================
        # DIGITAL TAP SETTINGS
        # =====================================

        self.pinch_threshold = 0.045

        self.tap_hold_time = 0.25

        self.tap_cooldown = 0.45

        # =====================================
        # HAND STATES
        # =====================================

        self.hand_states = {}

        self.last_tap_time = {}

        # =====================================
        # HAND ROLES
        # =====================================

        self.drawing_hand = None

        self.control_hand = None

    # =========================================
    # DISTANCE CALCULATION
    # =========================================

    def calculate_distance(self, point1, point2):

        dx = point1.x - point2.x

        dy = point1.y - point2.y

        return math.sqrt(
            dx * dx + dy * dy
        )

    # =========================================
    # AUTOMATIC HAND MODE DETECTION
    # =========================================

    def detect_hand_mode(self, hand_count):

        self.hand_count = hand_count

        if hand_count <= 0:

            self.mode = "NO_HAND"

            self.is_drawing_allowed = False

            self.drawing_hand = None

            self.control_hand = None

        elif hand_count == 1:

            self.mode = "SINGLE_HAND"

            self.is_drawing_allowed = True

            self.control_hand = None

        else:

            self.mode = "TWO_HAND"

            self.is_drawing_allowed = True

        return self.mode

    # =========================================
    # AUTOMATIC HAND ROLE DETECTION
    # =========================================

    def assign_hand_roles(self, handedness_list):

        """
        Assign roles using MediaPipe handedness.

        Single Hand:
            Available hand = Drawing

        Two Hands:
            Right Hand = Drawing
            Left Hand = Controls

        Fallback:
            If Right hand is unavailable,
            available hand becomes Drawing.
        """

        roles = {
            "drawing_hand": None,
            "control_hand": None
        }

        if not handedness_list:

            self.drawing_hand = None

            self.control_hand = None

            return roles

        detected_hands = []

        for index, handedness in enumerate(handedness_list):

            try:

                label = (
                    handedness.classification[0].label
                )

            except (AttributeError, IndexError, TypeError):

                continue

            detected_hands.append({
                "id": index,
                "hand": label
            })

        # Single hand mode

        if len(detected_hands) == 1:

            roles["drawing_hand"] = detected_hands[0]["id"]

        # Two hand mode

        elif len(detected_hands) >= 2:

            for hand in detected_hands:

                if hand["hand"] == "Right":

                    roles["drawing_hand"] = hand["id"]

                elif hand["hand"] == "Left":

                    roles["control_hand"] = hand["id"]

            # Fallback

            if roles["drawing_hand"] is None:

                roles["drawing_hand"] = detected_hands[0]["id"]

                if len(detected_hands) > 1:

                    roles["control_hand"] = detected_hands[1]["id"]

        self.drawing_hand = roles["drawing_hand"]

        self.control_hand = roles["control_hand"]

        return roles

    # =========================================
    # DIGITAL TAP DETECTION
    # =========================================

    def detect_digital_tap(self, landmarks, hand_id=0):

        """
        Digital Tap:

        Thumb + Index Finger Pinch.

        Tap registers after:
        1. Pinch starts.
        2. Pinch is held.
        3. Pinch is released.
        4. Cooldown has passed.
        """

        if landmarks is None:

            self.hand_states.pop(hand_id, None)

            return False

        points = landmarks.landmark

        thumb_tip = points[4]

        index_tip = points[8]

        distance = self.calculate_distance(
            thumb_tip,
            index_tip
        )

        current_time = time.monotonic()

        is_pinching = (
            distance < self.pinch_threshold
        )

        if hand_id not in self.hand_states:

            self.hand_states[hand_id] = {

                "pinching": False,

                "start_time": 0,

                "tap_ready": False

            }

        state = self.hand_states[hand_id]

        # Pinch begins

        if is_pinching and not state["pinching"]:

            state["pinching"] = True

            state["start_time"] = current_time

            state["tap_ready"] = False

        # Pinch held

        if is_pinching and state["pinching"]:

            held_time = (
                current_time - state["start_time"]
            )

            if held_time >= self.tap_hold_time:

                state["tap_ready"] = True

        # Pinch released

        if not is_pinching and state["pinching"]:

            state["pinching"] = False

            last_tap = self.last_tap_time.get(
                hand_id,
                0
            )

            cooldown_passed = (
                current_time - last_tap
                >= self.tap_cooldown
            )

            if state["tap_ready"] and cooldown_passed:

                self.last_tap_time[hand_id] = current_time

                state["tap_ready"] = False

                return True

            state["tap_ready"] = False

        return False

    # =========================================
    # PINCH STATUS
    # =========================================

    def is_pinching(self, landmarks):

        if landmarks is None:

            return False

        points = landmarks.landmark

        distance = self.calculate_distance(
            points[4],
            points[8]
        )

        return distance < self.pinch_threshold

    # =========================================
    # RESET CONTROLLER
    # =========================================

    def reset(self):

        self.mode = "NO_HAND"

        self.hand_count = 0

        self.is_drawing_allowed = False

        self.drawing_hand = None

        self.control_hand = None

        self.hand_states.clear()

        self.last_tap_time.clear()

    # =========================================
    # CONTROLLER INFORMATION
    # =========================================

    def get_status(self):

        return {

            "mode": self.mode,

            "hand_count": self.hand_count,

            "drawing_allowed": self.is_drawing_allowed,

            "drawing_hand": self.drawing_hand,

            "control_hand": self.control_hand

        }
