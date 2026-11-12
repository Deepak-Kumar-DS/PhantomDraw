"""
PhantomDraw AI
Advanced Brush Manager
Includes Color Selection History
"""


class BrushManager:

    def __init__(self):

        self.brushes = {
            "PENCIL": {"size": 3},
            "FINE": {"size": 2},
            "MARKER": {"size": 12},
            "NEON": {"size": 8},
            "THICK": {"size": 20}
        }

        # OpenCV BGR colors
        self.colors = {
            "GREEN": (0, 255, 0),
            "RED": (0, 0, 255),
            "BLUE": (255, 0, 0),
            "YELLOW": (0, 255, 255),
            "WHITE": (255, 255, 255),
            "PURPLE": (255, 0, 255),
            "ORANGE": (0, 165, 255),
            "CYAN": (255, 255, 0),
            "PINK": (203, 192, 255),
            "LIME": (0, 255, 128),
            "MAGENTA": (255, 0, 255),
            "GOLD": (0, 215, 255)
        }

        self.current_brush = "PENCIL"
        self.current_color = "WHITE"
        self.current_size = 3

        # Color history
        self.color_history = ["WHITE"]
        self.history_index = 0

    # ==========================================
    # BRUSH SELECTION
    # ==========================================

    def select_brush(self, brush_name):

        brush_name = brush_name.upper()

        if brush_name not in self.brushes:
            return False

        self.current_brush = brush_name

        self.current_size = self.brushes[brush_name]["size"]

        return True

    # ==========================================
    # COLOR SELECTION
    # ==========================================

    def select_color(self, color_name):

        color_name = color_name.upper()

        if color_name not in self.colors:
            return False

        if color_name == self.current_color:
            return True

        # Remove forward history after a new selection
        self.color_history = self.color_history[
            :self.history_index + 1
        ]

        self.color_history.append(color_name)

        self.history_index = len(self.color_history) - 1

        self.current_color = color_name

        return True

    # ==========================================
    # CUSTOM COLOR
    # ==========================================

    def set_custom_color(self, color):

        if not isinstance(color, (tuple, list)):
            return False

        if len(color) != 3:
            return False

        try:
            color = tuple(
                max(0, min(255, int(value)))
                for value in color
            )
        except (TypeError, ValueError):
            return False

        self.colors["CUSTOM"] = color

        self.select_color("CUSTOM")

        return True

    # ==========================================
    # PREVIOUS COLOR
    # ==========================================

    def previous_color(self):

        if self.history_index <= 0:
            return False

        self.history_index -= 1

        self.current_color = self.color_history[
            self.history_index
        ]

        return True

    # ==========================================
    # NEXT COLOR
    # ==========================================

    def next_color(self):

        if self.history_index >= len(self.color_history) - 1:
            return False

        self.history_index += 1

        self.current_color = self.color_history[
            self.history_index
        ]

        return True

    # ==========================================
    # COLOR HISTORY INFORMATION
    # ==========================================

    def get_color_history_info(self):

        return {
            "current_index": self.history_index,
            "total": len(self.color_history),
            "can_go_back": self.history_index > 0,
            "can_go_forward": (
                self.history_index < len(self.color_history) - 1
            )
        }

    # ==========================================
    # BRUSH SIZE
    # ==========================================

    def set_size(self, size):

        self.current_size = max(
            1,
            min(50, int(size))
        )

        return self.current_size

    # ==========================================
    # GET COLOR
    # ==========================================

    def get_color(self):

        return self.colors[self.current_color]

    # ==========================================
    # GET SETTINGS
    # ==========================================

    def get_settings(self):

        return {
            "brush": self.current_brush,
            "color": self.get_color(),
            "color_name": self.current_color,
            "size": self.current_size
        }

    # ==========================================
    # AVAILABLE COLORS
    # ==========================================

    def get_available_colors(self):

        return {
            name: color
            for name, color in self.colors.items()
            if name != "BLACK"
        }

    # ==========================================
    # AVAILABLE BRUSHES
    # ==========================================

    def get_available_brushes(self):

        return list(self.brushes.keys())