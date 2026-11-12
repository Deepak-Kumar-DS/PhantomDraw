"""
PhantomDraw AI
Advanced Gesture Drawing System

Features:
- Air Drawing
- Hand Tracking
- Color Palette
- Mouse Color Selection
- Color History Back / Next
- Brush Presets
- Undo / Redo
- Eraser
- Brush Size Control
"""

import cv2

from vision.camera import Camera
from vision.hand_tracking import HandTracker
from vision.gesture_detection import GestureDetector

from core.drawing_engine import DrawingEngine
from tools.brush import BrushManager


# =====================================================
# INITIALIZATION
# =====================================================

print("\n====================================")
print("         PHANTOMDRAW AI")
print("====================================")

camera = Camera()

tracker = HandTracker()

gesture_detector = GestureDetector()

drawing = DrawingEngine(
    width=1280,
    height=720
)

brush = BrushManager()

eraser_enabled = False

current_gesture = "NO HAND"

window_name = "PhantomDraw AI - Drawing Studio"

palette_buttons = []


# =====================================================
# MOUSE CALLBACK
# =====================================================

def mouse_callback(event, x, y, flags, parameter):

    global palette_buttons

    if event != cv2.EVENT_LBUTTONDOWN:
        return

    for button in palette_buttons:

        x1, y1, x2, y2 = button["position"]

        if x1 <= x <= x2 and y1 <= y <= y2:

            action = button["action"]

            if action == "COLOR":

                brush.select_color(button["name"])

                print("Selected:", button["name"])

            elif action == "BACK":

                if brush.previous_color():
                    print("Previous color:", brush.get_settings()["color_name"])
                else:
                    print("No previous color!")

            elif action == "NEXT":

                if brush.next_color():
                    print("Next color:", brush.get_settings()["color_name"])
                else:
                    print("No next color!")

            break


# =====================================================
# COLOR PALETTE
# =====================================================

def draw_color_palette(frame):

    global palette_buttons

    palette_buttons = []

    height, width = frame.shape[:2]

    panel_x = width - 405
    panel_y = 15

    panel_width = 390
    panel_height = 205

    # Panel background

    cv2.rectangle(
        frame,
        (panel_x, panel_y),
        (panel_x + panel_width, panel_y + panel_height),
        (25, 25, 25),
        -1
    )

    cv2.rectangle(
        frame,
        (panel_x, panel_y),
        (panel_x + panel_width, panel_y + panel_height),
        (0, 255, 100),
        2
    )

    cv2.putText(
        frame,
        "COLOR STUDIO",
        (panel_x + 15, panel_y + 25),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 255, 100),
        2
    )

    # Current color

    settings = brush.get_settings()

    current_color = settings["color"]

    cv2.rectangle(
        frame,
        (panel_x + 265, panel_y + 7),
        (panel_x + 370, panel_y + 32),
        current_color,
        -1
    )

    # Available colors

    colors = brush.get_available_colors()

    color_names = list(colors.keys())

    button_width = 58
    button_height = 35

    gap_x = 12
    gap_y = 13

    start_x = panel_x + 14
    start_y = panel_y + 45

    for index, color_name in enumerate(color_names):

        row = index // 5
        column = index % 5

        x1 = start_x + column * (button_width + gap_x)
        y1 = start_y + row * (button_height + gap_y)

        x2 = x1 + button_width
        y2 = y1 + button_height

        color = colors[color_name]

        # Color button

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            -1
        )

        # Selected color border

        if color_name == settings["color_name"]:

            border = (0, 255, 100)
            thickness = 4

        else:

            border = (255, 255, 255)
            thickness = 1

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            border,
            thickness
        )

        # Color label

        cv2.putText(
            frame,
            color_name[:3],
            (x1 + 5, y2 + 12),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.32,
            (255, 255, 255),
            1
        )

        palette_buttons.append({
            "name": color_name,
            "action": "COLOR",
            "position": (x1, y1, x2, y2)
        })

    # =============================================
    # COLOR HISTORY BUTTONS
    # =============================================

    history = brush.get_color_history_info()

    button_y = panel_y + 165

    back_color = (
        (0, 180, 255)
        if history["can_go_back"]
        else (70, 70, 70)
    )

    next_color = (
        (0, 180, 255)
        if history["can_go_forward"]
        else (70, 70, 70)
    )

    # BACK button

    cv2.rectangle(
        frame,
        (panel_x + 15, button_y),
        (panel_x + 165, button_y + 28),
        back_color,
        -1
    )

    cv2.putText(
        frame,
        "< BACK",
        (panel_x + 52, button_y + 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )

    palette_buttons.append({
        "name": "BACK",
        "action": "BACK",
        "position": (
            panel_x + 15,
            button_y,
            panel_x + 165,
            button_y + 28
        )
    })

    # NEXT button

    cv2.rectangle(
        frame,
        (panel_x + 205, button_y),
        (panel_x + 355, button_y + 28),
        next_color,
        -1
    )

    cv2.putText(
        frame,
        "NEXT >",
        (panel_x + 245, button_y + 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )

    palette_buttons.append({
        "name": "NEXT",
        "action": "NEXT",
        "position": (
            panel_x + 205,
            button_y,
            panel_x + 355,
            button_y + 28
        )
    })

    return frame


# =====================================================
# STATUS PANEL
# =====================================================

def draw_status_panel(frame, gesture, settings, eraser):

    x = 10
    y = 10

    cv2.rectangle(
        frame,
        (x, y),
        (430, 270),
        (25, 25, 25),
        -1
    )

    cv2.rectangle(
        frame,
        (x, y),
        (430, 270),
        (0, 255, 100),
        2
    )

    cv2.putText(
        frame,
        "PHANTOMDRAW AI",
        (25, 42),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 100),
        2
    )

    cv2.putText(
        frame,
        f"Gesture: {gesture}",
        (25, 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        f"Brush: {settings['brush']}",
        (25, 112),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        f"Size: {settings['size']}",
        (25, 144),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1
    )

    # Color preview

    cv2.rectangle(
        frame,
        (25, 165),
        (70, 200),
        settings["color"],
        -1
    )

    cv2.putText(
        frame,
        f"Color: {settings['color_name']}",
        (85, 190),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        1
    )

    cv2.putText(
        frame,
        f"Eraser: {'ON' if eraser else 'OFF'}",
        (25, 235),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 200, 255),
        1
    )

    return frame


# =====================================================
# KEYBOARD CONTROLS HELP
# =====================================================

def show_controls():

    print("""
========================================
          PHANTOMDRAW CONTROLS
========================================

BRUSHES
1 - Pencil
2 - Fine
3 - Marker
4 - Neon
5 - Thick

COLORS
G - Green
R - Red
B - Blue
T - Yellow
W - White
P - Purple
O - Orange

COLOR HISTORY
[ - Previous Color
] - Next Color

MOUSE
Click color - Select
Click BACK - Previous color
Click NEXT - Next color

DRAWING
+ - Increase size
- - Decrease size
E - Eraser
C - Clear
U - Undo
V - Redo
Q - Quit

========================================
""")


# =====================================================
# START CAMERA
# =====================================================

if not camera.start():

    print("Camera could not start!")

    tracker.close()

    raise SystemExit


cv2.namedWindow(
    window_name,
    cv2.WINDOW_NORMAL
)

cv2.resizeWindow(
    window_name,
    1280,
    720
)

cv2.setMouseCallback(
    window_name,
    mouse_callback
)

show_controls()

print("PhantomDraw AI started successfully!")


# =====================================================
# MAIN LOOP
# =====================================================

try:

    while True:

        # Camera

        success, frame = camera.read()

        if not success:
            print("Camera frame unavailable!")
            break

        # Hand tracking

        tracker.process_frame(frame)

        tracker.draw_landmarks(frame)

        hand_count = tracker.get_hand_count()

        # Gesture detection

        if hand_count > 0:

            landmarks = tracker.get_landmarks(0)

            gesture = gesture_detector.detect_gesture(
                landmarks
            )

            current_gesture = gesture

            if gesture == "DRAW":

                position = tracker.get_finger_position(
                    hand_index=0,
                    finger_id=8
                )

                if position is not None:

                    x = int(position[0] * drawing.width)
                    y = int(position[1] * drawing.height)

                    drawing.draw(x, y)

            else:

                drawing.stop_drawing()

        else:

            current_gesture = "NO HAND"

            drawing.stop_drawing()

        # Apply brush settings

        settings = brush.get_settings()

        drawing.set_brush_color(settings["color"])

        drawing.set_brush_size(settings["size"])

        drawing.set_brush_type(settings["brush"])

        # Combine canvas

        output = drawing.combine_frame(frame)

        # Status panel

        output = draw_status_panel(
            output,
            current_gesture,
            settings,
            eraser_enabled
        )

        # Color palette

        output = draw_color_palette(output)

        # Creator credit

        cv2.putText(
            output,
            "Developed by Deepak Kumar Sharma",
            (15, output.shape[0] - 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.45,
            (220, 220, 220),
            1
        )

        # Display

        cv2.imshow(window_name, output)

        # Keyboard

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

        # Clear

        elif key == ord("c"):
            drawing.clear_canvas()
            print("Canvas cleared!")

        # Drawing undo

        elif key == ord("u"):
            drawing.undo()
            print("Drawing undo!")

        # Drawing redo

        elif key == ord("v"):
            drawing.redo()
            print("Drawing redo!")

        # Previous color

        elif key == ord("["):

            if brush.previous_color():
                print("Previous color:", brush.get_settings()["color_name"])
            else:
                print("No previous color!")

        # Next color

        elif key == ord("]"):

            if brush.next_color():
                print("Next color:", brush.get_settings()["color_name"])
            else:
                print("No next color!")

        # Brush presets

        elif key == ord("1"):
            brush.select_brush("PENCIL")

        elif key == ord("2"):
            brush.select_brush("FINE")

        elif key == ord("3"):
            brush.select_brush("MARKER")

        elif key == ord("4"):
            brush.select_brush("NEON")

        elif key == ord("5"):
            brush.select_brush("THICK")

        # Colors

        elif key == ord("g"):
            brush.select_color("GREEN")

        elif key == ord("r"):
            brush.select_color("RED")

        elif key == ord("b"):
            brush.select_color("BLUE")

        elif key == ord("t"):
            brush.select_color("YELLOW")

        elif key == ord("w"):
            brush.select_color("WHITE")

        elif key == ord("p"):
            brush.select_color("PURPLE")

        elif key == ord("o"):
            brush.select_color("ORANGE")

        # Brush size

        elif key in (ord("+"), ord("=")):

            brush.set_size(
                brush.get_settings()["size"] + 2
            )

        elif key in (ord("-"), ord("_")):

            brush.set_size(
                brush.get_settings()["size"] - 2
            )

        # Eraser

        elif key == ord("e"):

            eraser_enabled = not eraser_enabled

            drawing.enable_eraser(eraser_enabled)

            drawing.stop_drawing()

            print(
                "Eraser:",
                "ON" if eraser_enabled else "OFF"
            )


# =====================================================
# ERROR HANDLING
# =====================================================

except KeyboardInterrupt:

    print("Application interrupted!")

except Exception as error:

    print("APPLICATION ERROR:", error)


# =====================================================
# CLEANUP
# =====================================================

finally:

    camera.stop()

    tracker.close()

    cv2.destroyAllWindows()

    print("PhantomDraw AI stopped.")