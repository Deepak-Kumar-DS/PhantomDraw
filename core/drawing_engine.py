"""
PhantomDraw AI
Advanced Multi-Hand Drawing Engine

Features:
- Simultaneous Two-Hand Drawing
- Independent Hand Tracking
- Multiple Brush Types
- Neon Glow
- Multi-Layer Drawing
- Per-Layer Undo and Redo
- Eraser
- Automatic Shape Correction
- Circle / Square / Rectangle / Triangle / Line Recognition
- Image Export
"""

import cv2
import numpy as np
import math

from core.history_manager import HistoryManager
from core.layer_manager import LayerManager


class DrawingEngine:

    def __init__(self, width=1280, height=720):

        self.width = width
        self.height = height

        self.layer_manager = LayerManager(
            width,
            height
        )

        self.layer_histories = {
            0: HistoryManager(max_history=30)
        }

        # Brush settings
        self.brush_color = (255, 255, 255)
        self.brush_size = 3
        self.brush_type = "PENCIL"

        # Independent drawing positions
        self.previous_positions = {}

        # Independent stroke points
        self.stroke_points = {}

        # Independent stroke history flags
        self.stroke_saved = set()

        # Eraser
        self.eraser_mode = False

        # Auto shape correction
        self.auto_shape_enabled = True

        # Shape recognition sensitivity
        self.shape_tolerance = 0.045

    # ==================================================
    # BACKWARD COMPATIBILITY
    # ==================================================

    @property
    def canvas(self):

        return self.layer_manager.get_active_canvas()

    @canvas.setter
    def canvas(self, value):

        self.layer_manager.layers[
            self.layer_manager.active_index
        ]["canvas"] = value

    @property
    def history(self):

        return self.layer_histories[
            self.layer_manager.active_index
        ]

    @property
    def previous_position(self):

        return self.previous_positions.get(0)

    @previous_position.setter
    def previous_position(self, value):

        if value is None:
            self.previous_positions.pop(0, None)
        else:
            self.previous_positions[0] = value

    # ==================================================
    # BRUSH SETTINGS
    # ==================================================

    def set_brush_color(self, color):

        self.brush_color = tuple(color)

    def set_brush_size(self, size):

        self.brush_size = max(
            1,
            min(50, int(size))
        )

    def set_brush_type(self, brush_type):

        self.brush_type = str(
            brush_type
        ).upper()

    # ==================================================
    # ERASER
    # ==================================================

    def enable_eraser(self, enabled=True):

        self.eraser_mode = bool(enabled)

    # ==================================================
    # AUTO SHAPE SETTINGS
    # ==================================================

    def enable_auto_shape(self, enabled=True):

        self.auto_shape_enabled = bool(enabled)

    def set_shape_tolerance(self, value):

        self.shape_tolerance = max(
            0.01,
            min(0.15, float(value))
        )

    # ==================================================
    # LAYER MANAGEMENT
    # ==================================================

    def add_layer(self, name=None):

        self.stop_drawing()

        index = self.layer_manager.add_layer(name)

        self.layer_histories[index] = HistoryManager(
            max_history=30
        )

        return index

    def remove_layer(self, index=None):

        self.stop_drawing()

        if index is None:
            index = self.layer_manager.active_index

        success = self.layer_manager.remove_layer(index)

        if success:

            self.layer_histories = {
                i: HistoryManager(max_history=30)
                for i in range(
                    len(self.layer_manager.layers)
                )
            }

        return success

    def set_active_layer(self, index):

        self.stop_drawing()

        return self.layer_manager.set_active_layer(
            index
        )

    def rename_layer(self, index, new_name):

        return self.layer_manager.rename_layer(
            index,
            new_name
        )

    def set_layer_visibility(self, index, visible):

        self.stop_drawing()

        return self.layer_manager.set_visibility(
            index,
            visible
        )

    def set_layer_opacity(self, index, opacity):

        return self.layer_manager.set_opacity(
            index,
            opacity
        )

    def get_layers_info(self):

        return self.layer_manager.get_layers_info()

    def get_layer_count(self):

        return len(self.layer_manager.layers)

    def get_active_layer_index(self):

        return self.layer_manager.active_index

    # ==================================================
    # NORMAL DRAWING
    # ==================================================

    def draw_normal_line(
        self,
        x1,
        y1,
        x2,
        y2
    ):

        cv2.line(
            self.canvas,
            (x1, y1),
            (x2, y2),
            self.brush_color,
            self.brush_size,
            cv2.LINE_AA
        )

    # ==================================================
    # NEON DRAWING
    # ==================================================

    def draw_neon_line(
        self,
        x1,
        y1,
        x2,
        y2
    ):

        padding = max(
            15,
            self.brush_size * 5
        )

        left = max(
            0,
            min(x1, x2) - padding
        )

        right = min(
            self.width,
            max(x1, x2) + padding + 1
        )

        top = max(
            0,
            min(y1, y2) - padding
        )

        bottom = min(
            self.height,
            max(y1, y2) + padding + 1
        )

        if right <= left or bottom <= top:
            return

        roi = self.canvas[
            top:bottom,
            left:right
        ]

        overlay = np.zeros_like(roi)

        cv2.line(
            overlay,
            (x1 - left, y1 - top),
            (x2 - left, y2 - top),
            self.brush_color,
            max(3, self.brush_size * 3),
            cv2.LINE_AA
        )

        glow = cv2.GaussianBlur(
            overlay,
            (0, 0),
            sigmaX=max(
                3,
                self.brush_size * 1.2
            )
        )

        combined = cv2.addWeighted(
            roi.copy(),
            1.0,
            glow,
            1.0,
            0
        )

        self.canvas[
            top:bottom,
            left:right
        ] = combined

        cv2.line(
            self.canvas,
            (x1, y1),
            (x2, y2),
            self.brush_color,
            max(1, self.brush_size // 2),
            cv2.LINE_AA
        )

    # ==================================================
    # DRAWING LINE
    # ==================================================

    def draw_line(
        self,
        x1,
        y1,
        x2,
        y2
    ):

        if self.eraser_mode:

            cv2.line(
                self.canvas,
                (x1, y1),
                (x2, y2),
                (0, 0, 0),
                self.brush_size * 4,
                cv2.LINE_AA
            )

        elif self.brush_type == "NEON":

            self.draw_neon_line(
                x1,
                y1,
                x2,
                y2
            )

        else:

            self.draw_normal_line(
                x1,
                y1,
                x2,
                y2
            )

    # ==================================================
    # DRAWING WITH MULTIPLE HANDS
    # ==================================================

    def draw(
        self,
        x,
        y,
        hand_id=0
    ):

        x = int(x)
        y = int(y)

        hand_id = int(hand_id)

        if not (
            0 <= x < self.width
            and 0 <= y < self.height
        ):

            self.stop_drawing(hand_id)

            return

        # First point of a new stroke
        if hand_id not in self.previous_positions:

            self.history.save_state(
                self.canvas
            )

            self.stroke_saved.add(hand_id)

            self.previous_positions[hand_id] = (
                x,
                y
            )

            self.stroke_points[hand_id] = [
                (x, y)
            ]

            return

        previous_x, previous_y = (
            self.previous_positions[hand_id]
        )

        # Draw this hand's stroke
        self.draw_line(
            previous_x,
            previous_y,
            x,
            y
        )

        self.previous_positions[hand_id] = (
            x,
            y
        )

        self.stroke_points.setdefault(
            hand_id,
            []
        ).append((x, y))

    # ==================================================
    # SHAPE RECOGNITION
    # ==================================================

    def recognize_shape(self, points):

        if points is None or len(points) < 8:
            return None

        contour = np.array(
            points,
            dtype=np.int32
        ).reshape((-1, 1, 2))

        perimeter = cv2.arcLength(
            contour,
            False
        )

        if perimeter < 50:
            return None

        x, y, w, h = cv2.boundingRect(
            contour
        )

        if w < 25 or h < 25:
            return None

        first = np.array(points[0])
        last = np.array(points[-1])

        closing_distance = np.linalg.norm(
            first - last
        )

        diagonal = math.sqrt(
            w * w + h * h
        )

        is_closed = (
            closing_distance
            < diagonal * 0.25
        )

        # ---------------------------------
        # STRAIGHT LINE
        # ---------------------------------

        if not is_closed:

            pts = np.array(
                points,
                dtype=np.float32
            )

            start = pts[0]
            end = pts[-1]

            line_vector = end - start

            line_length = np.linalg.norm(
                line_vector
            )

            if line_length < 50:
                return None

            distances = []

            for point in pts:

                distance = abs(
                    np.cross(
                        line_vector,
                        point - start
                    )
                ) / line_length

                distances.append(distance)

            average_error = np.mean(
                distances
            )

            if average_error < max(
                8,
                line_length * self.shape_tolerance
            ):

                return {
                    "type": "LINE",
                    "start": tuple(
                        start.astype(int)
                    ),
                    "end": tuple(
                        end.astype(int)
                    )
                }

            return None

        # Closed shape
        contour = np.array(
            points,
            dtype=np.int32
        ).reshape((-1, 1, 2))

        area = cv2.contourArea(
            contour
        )

        if area < 500:
            return None

        approximation = cv2.approxPolyDP(
            contour,
            0.035 * cv2.arcLength(
                contour,
                True
            ),
            True
        )

        vertices = len(approximation)

        # ---------------------------------
        # CIRCLE
        # ---------------------------------

        circularity = (
            4 * math.pi * area
            / (perimeter * perimeter)
        )

        aspect_ratio = w / float(h)

        if (
            circularity > 0.65
            and 0.75 < aspect_ratio < 1.33
        ):

            center = (
                x + w // 2,
                y + h // 2
            )

            radius = int(
                (w + h) / 4
            )

            return {
                "type": "CIRCLE",
                "center": center,
                "radius": radius
            }

        # ---------------------------------
        # TRIANGLE
        # ---------------------------------

        if vertices == 3:

            return {
                "type": "TRIANGLE",
                "points": approximation.reshape(
                    (-1, 2)
                )
            }

        # ---------------------------------
        # SQUARE / RECTANGLE
        # ---------------------------------

        if vertices == 4:

            ratio = w / float(h)

            if 0.85 <= ratio <= 1.15:

                return {
                    "type": "SQUARE",
                    "x": x,
                    "y": y,
                    "width": min(w, h)
                }

            return {
                "type": "RECTANGLE",
                "x": x,
                "y": y,
                "width": w,
                "height": h
            }

        return None

    # ==================================================
    # DRAW CORRECTED SHAPE
    # ==================================================

    def draw_corrected_shape(self, shape):

        if shape is None:
            return False

        color = self.brush_color

        thickness = self.brush_size

        if self.eraser_mode:
            return False

        shape_type = shape["type"]

        # LINE
        if shape_type == "LINE":

            cv2.line(
                self.canvas,
                shape["start"],
                shape["end"],
                color,
                thickness,
                cv2.LINE_AA
            )

        # CIRCLE
        elif shape_type == "CIRCLE":

            cv2.circle(
                self.canvas,
                shape["center"],
                shape["radius"],
                color,
                thickness,
                cv2.LINE_AA
            )

        # SQUARE
        elif shape_type == "SQUARE":

            x = shape["x"]
            y = shape["y"]
            size = shape["width"]

            cv2.rectangle(
                self.canvas,
                (x, y),
                (x + size, y + size),
                color,
                thickness,
                cv2.LINE_AA
            )

        # RECTANGLE
        elif shape_type == "RECTANGLE":

            x = shape["x"]
            y = shape["y"]

            cv2.rectangle(
                self.canvas,
                (x, y),
                (x + shape["width"], y + shape["height"]),
                color,
                thickness,
                cv2.LINE_AA
            )

        # TRIANGLE
        elif shape_type == "TRIANGLE":

            points = np.array(
                shape["points"],
                dtype=np.int32
            )

            cv2.polylines(
                self.canvas,
                [points],
                True,
                color,
                thickness,
                cv2.LINE_AA
            )

        return True

    # ==================================================
    # FINISH STROKE
    # ==================================================

    def finish_stroke(self, hand_id=0):

        hand_id = int(hand_id)

        points = self.stroke_points.pop(
            hand_id,
            []
        )

        self.previous_positions.pop(
            hand_id,
            None
        )

        self.stroke_saved.discard(
            hand_id
        )

        if (
            self.auto_shape_enabled
            and not self.eraser_mode
            and points
        ):

            shape = self.recognize_shape(
                points
            )

            if shape is not None:

                self.draw_corrected_shape(
                    shape
                )

                print(
                    "Auto Shape:",
                    shape["type"]
                )

                return shape["type"]

        return None

    # ==================================================
    # STOP DRAWING
    # ==================================================

    def stop_drawing(self, hand_id=None):

        if hand_id is None:

            hand_ids = list(
                self.previous_positions.keys()
            )

            for current_id in hand_ids:

                self.finish_stroke(
                    current_id
                )

        else:

            self.finish_stroke(
                hand_id
            )

    # ==================================================
    # UNDO
    # ==================================================

    def undo(self):

        self.stop_drawing()

        self.canvas = self.history.undo(
            self.canvas
        )

        return self.get_composite_canvas()

    # ==================================================
    # REDO
    # ==================================================

    def redo(self):

        self.stop_drawing()

        self.canvas = self.history.redo(
            self.canvas
        )

        return self.get_composite_canvas()

    # ==================================================
    # CLEAR
    # ==================================================

    def clear_canvas(self):

        self.stop_drawing()

        self.history.save_state(
            self.canvas
        )

        self.layer_manager.clear_layer()

        return self.get_composite_canvas()

    # ==================================================
    # ACTIVE CANVAS
    # ==================================================

    def get_active_canvas(self):

        return self.canvas

    # ==================================================
    # COMPOSITE CANVAS
    # ==================================================

    def get_composite_canvas(self):

        return self.layer_manager.get_composite()

    def get_canvas(self):

        return self.get_composite_canvas()

    # ==================================================
    # CAMERA + DRAWING
    # ==================================================

    def combine_frame(self, frame):

        canvas = self.get_composite_canvas()

        if frame.shape[:2] != canvas.shape[:2]:

            canvas = cv2.resize(
                canvas,
                (
                    frame.shape[1],
                    frame.shape[0]
                )
            )

        return cv2.addWeighted(
            frame,
            1.0,
            canvas,
            1.0,
            0
        )

    # ==================================================
    # SAVE
    # ==================================================

    def save_canvas(
        self,
        filename="drawing.png"
    ):

        return cv2.imwrite(
            filename,
            self.get_composite_canvas()
        )

    # ==================================================
    # HISTORY INFORMATION
    # ==================================================

    def get_history_info(self):

        return self.history.get_history_info()