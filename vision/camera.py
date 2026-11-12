
"""
PhantomDraw AI
Camera Module

Handles webcam initialization, frame capture
and camera resource management.
"""

import cv2


class Camera:

    def __init__(
        self,
        camera_index=0,
        width=1280,
        height=720
    ):
        self.camera_index = camera_index
        self.width = width
        self.height = height

        self.capture = None
        self.is_running = False

    def start(self):
        """Initialize and start the webcam."""

        if self.is_running:
            return True

        self.capture = cv2.VideoCapture(
            self.camera_index,
            cv2.CAP_DSHOW
        )

        if not self.capture.isOpened():
            self.capture.release()
            self.capture = None
            print("ERROR: Camera could not be opened.")
            return False

        self.capture.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            self.width
        )

        self.capture.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            self.height
        )

        self.is_running = True

        print("Camera started successfully!")
        return True

    def read(self):
        """Read one frame from the webcam."""

        if not self.is_running or self.capture is None:
            return False, None

        success, frame = self.capture.read()

        if not success:
            return False, None

        # Mirror the webcam image
        frame = cv2.flip(frame, 1)

        return True, frame

    def get_frame_size(self):
        """Return current camera frame dimensions."""

        if self.capture is None:
            return None

        width = int(
            self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        return width, height

    def stop(self):
        """Release webcam resources."""

        if self.capture is not None:
            self.capture.release()
            self.capture = None

        self.is_running = False

        print("Camera stopped.")

    def __del__(self):
        """Ensure camera is released."""

        self.stop()
