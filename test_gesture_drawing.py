"""
PhantomDraw AI
Two-Hand Gesture Controlled Air Drawing

HAND 1:
- Air Drawing

HAND 2:
- Thumb Up UI Selection

UI:
- Compact Status Board: Top Left
- Small 2D Settings Icon: Below Status Board
- Hover + Thumb Hold Selection

Mouse Controls: Disabled
"""

import cv2
import os
import time
import math
import traceback

from vision.camera import Camera
from vision.hand_tracking import HandTracker
from vision.gesture_detection import GestureDetector
from vision.interaction_controller import InteractionController

from core.drawing_engine import DrawingEngine
from tools.brush import BrushManager


# =====================================================
# INITIALIZATION
# =====================================================

print("\n====================================")
print("          PHANTOMDRAW AI")
print("====================================")

camera = Camera()
tracker = HandTracker()
gesture_detector = GestureDetector()
interaction = InteractionController()

drawing = DrawingEngine(
    width=1280,
    height=720
)

brush = BrushManager()

window_name = "PhantomDraw AI"

settings_open = False

eraser_enabled = False
auto_shape_enabled = True

current_mode = "NO_HAND"
current_gesture = "NO HAND"

buttons = []
hand_status = []

hover_state = {
    "action": None,
    "start_time": 0,
    "fired": False
}

HOVER_SELECT_TIME = 0.65

hover_progress_by_action = {}

selected_control_status = "WAITING"


# =====================================================
# UI HELPERS
# =====================================================

def draw_text(
    frame,
    text,
    position,
    scale=0.5,
    color=(255, 255, 255),
    thickness=1
):

    cv2.putText(
        frame,
        str(text),
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        scale,
        color,
        thickness,
        cv2.LINE_AA
    )


def point_inside(point, rectangle):

    x, y = point

    x1, y1, x2, y2 = rectangle

    return (
        x1 <= x <= x2
        and y1 <= y <= y2
    )


def find_button(point):

    for button in buttons:

        if point_inside(
            point,
            button["position"]
        ):

            return button

    return None


def draw_button(
    frame,
    label,
    position,
    action,
    selected=False
):

    global buttons

    x1, y1, x2, y2 = position

    progress = hover_progress_by_action.get(
        action,
        0
    )

    is_hovered = progress > 0

    if selected or is_hovered:

        background = (45, 85, 85)
        border = (0, 255, 190)

    else:

        background = (42, 45, 55)
        border = (110, 120, 135)

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        background,
        -1
    )

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        border,
        2 if is_hovered or selected else 1
    )

    text_size = cv2.getTextSize(
        label,
        cv2.FONT_HERSHEY_SIMPLEX,
        0.40,
        1
    )[0]

    text_x = x1 + (
        x2 - x1 - text_size[0]
    ) // 2

    text_y = y1 + (
        y2 - y1 + text_size[1]
    ) // 2

    draw_text(
        frame,
        label,
        (text_x, text_y),
        0.40
    )

    if is_hovered:

        bar_width = int(
            (x2 - x1) * min(progress, 1)
        )

        cv2.rectangle(
            frame,
            (x1, y2 - 4),
            (x1 + bar_width, y2),
            (0, 255, 190),
            -1
        )

    buttons.append({
        "label": label,
        "action": action,
        "position": position
    })


# =====================================================
# SETTINGS BUTTON POSITION
# =====================================================

def get_settings_button(width):

    # Status dashboard ke just below

    return (
        15,
        280,
        65,
        325
    )


# =====================================================
# ACTION EXECUTION
# =====================================================

def execute_action(action):

    global settings_open
    global eraser_enabled
    global auto_shape_enabled
    global selected_control_status

    if action == "OPEN_SETTINGS":

        settings_open = True

        drawing.stop_drawing()

        selected_control_status = "SETTINGS OPENED"

        print("Settings opened!")

        return

    if action == "CLOSE":

        settings_open = False

        drawing.stop_drawing()

        selected_control_status = "SETTINGS CLOSED"

        print("Settings closed!")

        return

    # BRUSH

    if action.startswith("BRUSH:"):

        brush_name = action.split(":")[1]

        brush.select_brush(brush_name)

        drawing.stop_drawing()

        print("Brush:", brush_name)

    # COLOR

    elif action.startswith("COLOR:"):

        color_name = action.split(":")[1]

        brush.select_color(color_name)

        drawing.stop_drawing()

        print("Color:", color_name)

    # BRUSH SIZE

    elif action == "SIZE_UP":

        settings = brush.get_settings()

        brush.set_size(
            settings["size"] + 2
        )

    elif action == "SIZE_DOWN":

        settings = brush.get_settings()

        brush.set_size(
            settings["size"] - 2
        )

    # ERASER

    elif action == "ERASER":

        eraser_enabled = not eraser_enabled

        drawing.enable_eraser(
            eraser_enabled
        )

        drawing.stop_drawing()

        print("Eraser:", eraser_enabled)

    # AUTO SHAPE

    elif action == "AUTO_SHAPE":

        auto_shape_enabled = not auto_shape_enabled

        drawing.enable_auto_shape(
            auto_shape_enabled
        )

        drawing.stop_drawing()

        print(
            "Auto Shape:",
            auto_shape_enabled
        )

    # UNDO

    elif action == "UNDO":

        drawing.stop_drawing()

        drawing.undo()

    # REDO

    elif action == "REDO":

        drawing.stop_drawing()

        drawing.redo()

    # CLEAR

    elif action == "CLEAR":

        drawing.stop_drawing()

        drawing.clear_canvas()

        print("Canvas cleared!")

    # ADD LAYER

    elif action == "LAYER_ADD":

        drawing.stop_drawing()

        drawing.add_layer()

        print("New layer added!")

    # PREVIOUS LAYER

    elif action == "LAYER_PREV":

        current = drawing.get_active_layer_index()

        if current > 0:

            drawing.set_active_layer(
                current - 1
            )

    # NEXT LAYER

    elif action == "LAYER_NEXT":

        current = drawing.get_active_layer_index()

        total = drawing.get_layer_count()

        if current < total - 1:

            drawing.set_active_layer(
                current + 1
            )

    # DELETE LAYER

    elif action == "LAYER_DELETE":

        if drawing.get_layer_count() > 1:

            drawing.remove_layer()

    # VISIBILITY

    elif action == "LAYER_VISIBILITY":

        index = drawing.get_active_layer_index()

        layers = drawing.get_layers_info()

        drawing.set_layer_visibility(
            index,
            not layers[index]["visible"]
        )

    # OPACITY

    elif action == "OPACITY_UP":

        index = drawing.get_active_layer_index()

        layers = drawing.get_layers_info()

        drawing.set_layer_opacity(
            index,
            min(
                1.0,
                layers[index]["opacity"] + 0.1
            )
        )

    elif action == "OPACITY_DOWN":

        index = drawing.get_active_layer_index()

        layers = drawing.get_layers_info()

        drawing.set_layer_opacity(
            index,
            max(
                0.0,
                layers[index]["opacity"] - 0.1
            )
        )

    # SAVE

    elif action == "SAVE":

        os.makedirs(
            "exports",
            exist_ok=True
        )

        success = drawing.save_canvas(
            "exports/phantomdraw.png"
        )

        if success:

            print("Drawing saved successfully!")

        else:

            print("Unable to save drawing!")

    selected_control_status = "SELECTED"


# =====================================================
# SETTINGS PANEL
# =====================================================

def draw_settings_panel(frame):

    global buttons

    buttons = []

    panel_x = 170
    panel_y = 65

    panel_width = 940
    panel_height = 550

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (panel_x, panel_y),
        (
            panel_x + panel_width,
            panel_y + panel_height
        ),
        (20, 22, 30),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.95,
        frame,
        0.05,
        0,
        frame
    )

    cv2.rectangle(
        frame,
        (panel_x, panel_y),
        (
            panel_x + panel_width,
            panel_y + panel_height
        ),
        (0, 200, 170),
        2
    )

    draw_text(
        frame,
        "PHANTOMDRAW SETTINGS",
        (panel_x + 25, panel_y + 35),
        0.8,
        (0, 230, 180),
        2
    )

    draw_text(
        frame,
        "THUMB UP TO SELECT",
        (panel_x + 25, panel_y + 62),
        0.42,
        (175, 185, 200)
    )

    draw_button(
        frame,
        "CLOSE X",
        (
            panel_x + 820,
            panel_y + 15,
            panel_x + 915,
            panel_y + 48
        ),
        "CLOSE"
    )

    # BRUSH PRESETS

    draw_text(
        frame,
        "BRUSH PRESETS",
        (panel_x + 25, panel_y + 105),
        0.5,
        (0, 220, 190)
    )

    brush_names = [
        "PENCIL",
        "FINE",
        "MARKER",
        "NEON",
        "THICK"
    ]

    settings = brush.get_settings()

    for index, name in enumerate(brush_names):

        x = panel_x + 25 + index * 135

        draw_button(
            frame,
            name,
            (
                x,
                panel_y + 118,
                x + 120,
                panel_y + 157
            ),
            f"BRUSH:{name}",
            selected=settings["brush"] == name
        )

    # COLORS

    draw_text(
        frame,
        "COLORS",
        (panel_x + 25, panel_y + 195),
        0.5,
        (0, 220, 190)
    )

    colors = brush.get_available_colors()

    color_names = list(colors.keys())

    for index, name in enumerate(color_names):

        row = index // 6
        column = index % 6

        x = panel_x + 25 + column * 145
        y = panel_y + 207 + row * 38

        color = colors[name]

        selected = name == settings["color_name"]

        progress = hover_progress_by_action.get(
            f"COLOR:{name}",
            0
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + 125, y + 30),
            color,
            -1
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x + 125, y + 30),
            (0, 255, 190)
            if selected or progress > 0
            else (180, 180, 180),
            2 if selected or progress > 0 else 1
        )

        if progress > 0:

            bar_width = int(
                125 * min(progress, 1)
            )

            cv2.rectangle(
                frame,
                (x, y + 26),
                (x + bar_width, y + 30),
                (0, 255, 190),
                -1
            )

        draw_text(
            frame,
            name,
            (x + 8, y + 20),
            0.38
        )

        buttons.append({
            "label": name,
            "action": f"COLOR:{name}",
            "position": (
                x,
                y,
                x + 125,
                y + 30
            )
        })

    # SIZE / ERASER / SHAPE

    size_y = panel_y + 305

    draw_text(
        frame,
        f"BRUSH SIZE: {settings['size']}",
        (panel_x + 25, size_y + 25),
        0.5
    )

    draw_button(
        frame,
        "SIZE -",
        (
            panel_x + 220,
            size_y,
            panel_x + 300,
            size_y + 38
        ),
        "SIZE_DOWN"
    )

    draw_button(
        frame,
        "SIZE +",
        (
            panel_x + 310,
            size_y,
            panel_x + 390,
            size_y + 38
        ),
        "SIZE_UP"
    )

    draw_button(
        frame,
        "ERASER ON" if eraser_enabled else "ERASER OFF",
        (
            panel_x + 440,
            size_y,
            panel_x + 585,
            size_y + 38
        ),
        "ERASER",
        selected=eraser_enabled
    )

    draw_button(
        frame,
        "SHAPE ON" if auto_shape_enabled else "SHAPE OFF",
        (
            panel_x + 605,
            size_y,
            panel_x + 765,
            size_y + 38
        ),
        "AUTO_SHAPE",
        selected=auto_shape_enabled
    )

    # DRAWING ACTIONS

    action_y = panel_y + 365

    draw_text(
        frame,
        "DRAWING ACTIONS",
        (panel_x + 25, action_y),
        0.5,
        (0, 220, 190)
    )

    actions = [
        ("UNDO", "UNDO"),
        ("REDO", "REDO"),
        ("CLEAR", "CLEAR"),
        ("SAVE PNG", "SAVE")
    ]

    for index, (label, action) in enumerate(actions):

        x = panel_x + 25 + index * 150

        draw_button(
            frame,
            label,
            (
                x,
                action_y + 12,
                x + 130,
                action_y + 52
            ),
            action
        )

    # LAYERS

    layer_y = panel_y + 450

    layers = drawing.get_layers_info()

    active_index = drawing.get_active_layer_index()

    active_layer = layers[active_index]

    draw_text(
        frame,
        f"LAYERS: {len(layers)} | ACTIVE: {active_layer['name']}",
        (panel_x + 25, layer_y),
        0.48,
        (0, 220, 190)
    )

    layer_actions = [
        ("ADD", "LAYER_ADD"),
        ("PREVIOUS", "LAYER_PREV"),
        ("NEXT", "LAYER_NEXT"),
        ("DELETE", "LAYER_DELETE"),
        (
            "HIDE" if active_layer["visible"] else "SHOW",
            "LAYER_VISIBILITY"
        ),
        ("OPACITY -", "OPACITY_DOWN"),
        ("OPACITY +", "OPACITY_UP")
    ]

    for index, (label, action) in enumerate(layer_actions):

        x = panel_x + 25 + index * 125

        draw_button(
            frame,
            label,
            (
                x,
                layer_y + 12,
                x + 112,
                layer_y + 50
            ),
            action
        )

    return frame


# =====================================================
# STATUS BOARD - TOP LEFT
# =====================================================

def draw_status_panel(frame):

    panel_x = 15
    panel_y = 65

    panel_width = 255
    panel_height = 205

    overlay = frame.copy()

    cv2.rectangle(
        overlay,
        (panel_x, panel_y),
        (
            panel_x + panel_width,
            panel_y + panel_height
        ),
        (15, 20, 28),
        -1
    )

    cv2.addWeighted(
        overlay,
        0.85,
        frame,
        0.15,
        0,
        frame
    )

    cv2.rectangle(
        frame,
        (panel_x, panel_y),
        (
            panel_x + panel_width,
            panel_y + panel_height
        ),
        (0, 200, 170),
        1
    )

    settings = brush.get_settings()

    layers = drawing.get_layers_info()

    active_index = drawing.get_active_layer_index()

    active_layer = layers[active_index]

    status_lines = [
        ("DRAWING STATUS", (0, 230, 180)),
        (f"Hands: {len(hand_status)}", (255, 255, 255)),
        (f"Mode: {current_mode}", (255, 255, 255)),
        (f"Brush: {settings['brush']}", (255, 255, 255)),
        (f"Size: {settings['size']}", (255, 255, 255)),
        (f"Color: {settings['color_name']}", (255, 255, 255)),
        (f"Gesture: {current_gesture}", (255, 255, 255)),
        (f"Layer: {active_layer['name']}", (255, 255, 255)),
        (
            "Auto Shape: ON"
            if auto_shape_enabled
            else "Auto Shape: OFF",
            (0, 230, 180)
            if auto_shape_enabled
            else (150, 150, 150)
        )
    ]

    for index, (text, color) in enumerate(status_lines):

        draw_text(
            frame,
            text,
            (
                panel_x + 13,
                panel_y + 23 + index * 20
            ),
            0.40,
            color,
            1
        )

    return frame


# =====================================================
# MAIN SCREEN
# =====================================================

def draw_main_screen(frame):

    height, width = frame.shape[:2]

    cv2.rectangle(
        frame,
        (0, 0),
        (width, 48),
        (20, 20, 25),
        -1
    )

    draw_text(
        frame,
        "PHANTOMDRAW AI",
        (20, 32),
        0.75,
        (0, 230, 180),
        2
    )

    # SMALL 2D SETTINGS ICON
    # Status board ke just below

    x1, y1, x2, y2 = get_settings_button(width)

    progress = hover_progress_by_action.get(
        "OPEN_SETTINGS",
        0
    )

    is_hovered = progress > 0

    background = (
        (40, 85, 80)
        if is_hovered
        else (35, 45, 55)
    )

    border = (
        (0, 255, 190)
        if is_hovered
        else (100, 180, 165)
    )

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        background,
        -1
    )

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        border,
        1
    )

    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2

    cv2.circle(
        frame,
        (center_x, center_y),
        9,
        (0, 230, 180),
        2
    )

    cv2.circle(
        frame,
        (center_x, center_y),
        3,
        (255, 255, 255),
        -1
    )

    for angle in range(0, 360, 45):

        rad = math.radians(angle)

        start_x = int(
            center_x + 10 * math.cos(rad)
        )

        start_y = int(
            center_y + 10 * math.sin(rad)
        )

        end_x = int(
            center_x + 14 * math.cos(rad)
        )

        end_y = int(
            center_y + 14 * math.sin(rad)
        )

        cv2.line(
            frame,
            (start_x, start_y),
            (end_x, end_y),
            (0, 230, 180),
            2
        )

    if is_hovered:

        bar_width = int(
            (x2 - x1) * min(progress, 1)
        )

        cv2.rectangle(
            frame,
            (x1, y2 - 3),
            (x1 + bar_width, y2),
            (0, 255, 190),
            -1
        )

    draw_text(
        frame,
        "Developed by Deepak Kumar Sharma",
        (15, height - 12),
        0.4,
        (220, 220, 220)
    )

    return frame


# =====================================================
# HOVER + THUMB UP SELECTION
# =====================================================

def update_hover_selection(
    control_position,
    control_gesture,
    frame_width
):

    global hover_state
    global hover_progress_by_action
    global selected_control_status

    now = time.monotonic()

    target = None

    if control_position is not None:

        if settings_open:

            target = find_button(
                control_position
            )

        else:

            settings_rectangle = get_settings_button(
                frame_width
            )

            if point_inside(
                control_position,
                settings_rectangle
            ):

                target = {
                    "action": "OPEN_SETTINGS",
                    "label": "SETTINGS"
                }

    if control_gesture != "THUMB_UP":

        hover_state = {
            "action": None,
            "start_time": 0,
            "fired": False
        }

        hover_progress_by_action = {}

        selected_control_status = "SHOW THUMB UP"

        return None

    if target is None:

        hover_state = {
            "action": None,
            "start_time": 0,
            "fired": False
        }

        hover_progress_by_action = {}

        selected_control_status = "POINT AT BUTTON"

        return None

    action = target["action"]

    if hover_state["action"] != action:

        hover_state = {
            "action": action,
            "start_time": now,
            "fired": False
        }

    elapsed = now - hover_state["start_time"]

    progress = min(
        elapsed / HOVER_SELECT_TIME,
        1.0
    )

    hover_progress_by_action = {
        action: progress
    }

    selected_control_status = (
        f"SELECTING {target.get('label', action)}"
    )

    if (
        elapsed >= HOVER_SELECT_TIME
        and not hover_state["fired"]
    ):

        hover_state["fired"] = True

        print(
            "Thumb selection:",
            action
        )

        execute_action(action)

        return action

    return None


# =====================================================
# CAMERA START
# =====================================================

if not camera.start():

    print("Camera could not start!")

    tracker.close()

    interaction.reset()

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

print("\nPhantomDraw AI started successfully!")

print("Hand 1: Air Drawing")
print("Hand 2: Thumb Up Selection")
print("Hover Selection: Enabled")
print("Mouse Controls: Disabled")
print("Auto Shape Correction: Enabled")


# =====================================================
# MAIN LOOP
# =====================================================

try:

    while True:

        # CAMERA

        success, frame = camera.read()

        if not success:

            print("Camera frame unavailable!")

            break

        height, width = frame.shape[:2]

        # HAND TRACKING

        tracker.process_frame(frame)

        tracker.draw_landmarks(frame)

        hand_count = tracker.get_hand_count()

        current_mode = interaction.detect_hand_mode(
            hand_count
        )

        # HAND INFORMATION

        hand_status = []

        gestures = {}

        for hand_index in range(hand_count):

            label = tracker.get_hand_label(
                hand_index
            )

            hand_status.append({
                "id": hand_index,
                "label": label
            })

            landmarks = tracker.get_landmarks(
                hand_index
            )

            if landmarks is None:
                continue

            gestures[hand_index] = (
                gesture_detector.detect_gesture(
                    landmarks
                )
            )

        # HAND ROLES

        control_position = None

        control_gesture = "UNKNOWN"

        if hand_count >= 2:

            # First hand = Drawing
            # Second hand = UI control

            first_hand = 0
            second_hand = 1

            thumb_position = tracker.get_finger_position(
                hand_index=second_hand,
                finger_id=4
            )

            if thumb_position is not None:

                control_position = (
                    int(thumb_position[0] * width),
                    int(thumb_position[1] * height)
                )

            control_gesture = gestures.get(
                second_hand,
                "UNKNOWN"
            )

            current_gesture = (
                f"H1: {gestures.get(first_hand, 'UNKNOWN')} | "
                f"H2: {control_gesture}"
            )

        elif hand_count == 1:

            current_gesture = gestures.get(
                0,
                "UNKNOWN"
            )

            hover_state = {
                "action": None,
                "start_time": 0,
                "fired": False
            }

            hover_progress_by_action = {}

            selected_control_status = "NEED SECOND HAND"

        else:

            current_gesture = "NO HAND"

            hover_state = {
                "action": None,
                "start_time": 0,
                "fired": False
            }

            hover_progress_by_action = {}

            selected_control_status = "NO HAND"

        # DRAWING WITH FIRST HAND ONLY

        if not settings_open:

            if hand_count >= 1:

                first_hand_landmarks = tracker.get_landmarks(
                    0
                )

                first_hand_gesture = gestures.get(
                    0,
                    "UNKNOWN"
                )

                if (
                    first_hand_landmarks is not None
                    and first_hand_gesture == "DRAW"
                ):

                    position = tracker.get_finger_position(
                        hand_index=0,
                        finger_id=8
                    )

                    if position is not None:

                        x = int(
                            position[0] * drawing.width
                        )

                        y = int(
                            position[1] * drawing.height
                        )

                        drawing.draw(
                            x,
                            y,
                            hand_id=0
                        )

                else:

                    drawing.stop_drawing(0)

            else:

                drawing.stop_drawing()

        else:

            drawing.stop_drawing()

        # HOVER + THUMB SELECTION

        update_hover_selection(
            control_position,
            control_gesture,
            width
        )

        # BRUSH SETTINGS

        settings = brush.get_settings()

        drawing.set_brush_color(
            settings["color"]
        )

        drawing.set_brush_size(
            settings["size"]
        )

        drawing.set_brush_type(
            settings["brush"]
        )

        # COMBINE CAMERA + DRAWING

        output = drawing.combine_frame(
            frame
        )

        # DISPLAY UI

        if settings_open:

            output = draw_settings_panel(
                output
            )

        else:

            buttons = []

            output = draw_main_screen(
                output
            )

            output = draw_status_panel(
                output
            )

        # SECOND HAND THUMB CURSOR

        if control_position is not None:

            px, py = control_position

            cv2.circle(
                output,
                (px, py),
                13,
                (0, 255, 190),
                2
            )

            cv2.circle(
                output,
                (px, py),
                4,
                (255, 255, 255),
                -1
            )

            draw_text(
                output,
                "CONTROL",
                (px + 15, py - 12),
                0.38,
                (0, 255, 190)
            )

        # STATUS

        if not settings_open:

            draw_text(
                output,
                selected_control_status,
                (290, 35),
                0.45,
                (0, 230, 180)
            )

        else:

            draw_text(
                output,
                selected_control_status,
                (190, 640),
                0.45,
                (0, 230, 180)
            )

        # DISPLAY

        cv2.imshow(
            window_name,
            output
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):

            break


# =====================================================
# ERROR HANDLING
# =====================================================

except KeyboardInterrupt:

    print("Application interrupted!")

except Exception as error:

    print("\nAPPLICATION ERROR:", error)

    traceback.print_exc()


# =====================================================
# CLEANUP
# =====================================================

finally:

    camera.stop()

    tracker.close()

    interaction.reset()

    cv2.destroyAllWindows()

    print("PhantomDraw AI stopped.")