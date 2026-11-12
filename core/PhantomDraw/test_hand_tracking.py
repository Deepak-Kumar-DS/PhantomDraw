import cv2

from vision.camera import Camera
from vision.hand_tracking import HandTracker


def main():

    camera = Camera()
    tracker = HandTracker()

    if not camera.start():
        print("Camera could not start!")
        tracker.close()
        return

    print("Live Hand Tracking Started!")
    print("Press Q to exit.")

    try:

        while True:

            success, frame = camera.read()

            if not success:
                print("Frame capture failed!")
                break

            # Detect hands
            tracker.process_frame(frame)

            # Draw hand landmarks
            frame = tracker.draw_landmarks(frame)

            # Get detected hand count
            hand_count = tracker.get_hand_count()

            cv2.putText(
                frame,
                f"Hands Detected: {hand_count}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "PhantomDraw AI - Hand Tracking",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    finally:

        camera.stop()
        tracker.close()
        cv2.destroyAllWindows()

        print("Live Hand Tracking Stopped!")


if __name__ == "__main__":
    main()