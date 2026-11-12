import cv2
import mediapipe as mp
import numpy as np

# MediaPipe Hands setup
mp_hands = mp.solutions.hands
hands = mp.solutions.hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Canvas initialize setup
canvas = None
x_prev, y_prev = 0, 0

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Frame ko flip karein taaki mirror effect mile
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    # BGR se RGB convert karein MediaPipe ke liye
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Index finger tip (Landmark 8) ki coordinates
            index_tip = hand_landmarks.landmark[8]
            x, y = int(index_tip.x * w), int(index_tip.y * h)

            if x_prev == 0 and y_prev == 0:
                x_prev, y_prev = x, y

            # Screen par green line draw karein
            cv2.line(canvas, (x_prev, y_prev), (x, y), (0, 255, 0), 5)
            x_prev, y_prev = x, y

            # Hand landmarks draw karein
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    else:
        x_prev, y_prev = 0, 0

    # Frame aur Canvas ko combine karein
    combined = cv2.add(frame, canvas)

    cv2.imshow("PhantomDraw - Air Drawing", combined)

    # 'q' key dabane par program band ho jayega
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()