import cv2

from vision.camera import Camera
from vision.hand_tracking import HandTracker
from core.drawing_engine import DrawingEngine


def main():

    camera = Camera()
    tracker = HandTracker()
    drawing = DrawingEngine()

    if not camera.start():
        print("Camera could not start!")
        tracker.close()
        return

    print("PhantomDraw Air Drawing Started!")
    print("Move your index finger to draw.")
    print("Press C to clear the canvas.")
    print("Press Q to quit.")

    try:

        while True:

            success, frame = camera.read()

            if not success:
                break

            tracker.process_frame(frame)

            landmarks = tracker.get_landmarks()

            if landmarks:

                # Index finger tip landmark = 8
                index_tip = landmarks.landmark[8]

                height, width, _ = frame.shape

                x = int(index_tip.x * width)
                y = int(index_tip.y * height)

                drawing.draw(x, y)

                cv2.circle(
                    frame,
                    (x, y),
                    10,
                    (0, 255, 0),
                    cv2.FILLED
                )

            else:

                drawing.stop_drawing()

            # Draw hand landmarks
            frame = tracker.draw_landmarks(frame)

            # Combine camera and drawing canvas
            output = drawing.combine_frame(frame)

            cv2.putText(
                output,
                "AIR DRAWING MODE",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 100),
                2
            )

            cv2.imshow(
                "PhantomDraw AI - Air Drawing",
                output
            )

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

            elif key == ord("c"):
                drawing.clear_canvas()
                print("Canvas cleared!")

    finally:

        camera.stop()
        tracker.close()
        cv2.destroyAllWindows()

        print("PhantomDraw stopped!")


if __name__ == "__main__":
    main()