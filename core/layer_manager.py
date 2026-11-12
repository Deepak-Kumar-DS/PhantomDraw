"""
PhantomDraw AI
Layer Management System
"""

import numpy as np


class LayerManager:

    def __init__(self, width=1280, height=720):

        self.width = width
        self.height = height

        self.layers = []
        self.active_index = 0

        # Create default layer
        self.add_layer("Background")

    # -----------------------------
    # CREATE NEW LAYER
    # -----------------------------

    def add_layer(self, name=None):

        if name is None:
            name = f"Layer {len(self.layers) + 1}"

        layer = {
            "name": name,
            "canvas": np.zeros(
                (self.height, self.width, 3),
                dtype=np.uint8
            ),
            "visible": True,
            "opacity": 1.0
        }

        self.layers.append(layer)
        self.active_index = len(self.layers) - 1

        return self.active_index

    # -----------------------------
    # DELETE LAYER
    # -----------------------------

    def remove_layer(self, index=None):

        if index is None:
            index = self.active_index

        if len(self.layers) <= 1:
            return False

        if not 0 <= index < len(self.layers):
            return False

        self.layers.pop(index)

        self.active_index = min(
            self.active_index,
            len(self.layers) - 1
        )

        return True

    # -----------------------------
    # SELECT ACTIVE LAYER
    # -----------------------------

    def set_active_layer(self, index):

        if not 0 <= index < len(self.layers):
            return False

        self.active_index = index
        return True

    # -----------------------------
    # GET ACTIVE CANVAS
    # -----------------------------

    def get_active_canvas(self):

        return self.layers[self.active_index]["canvas"]

    # -----------------------------
    # RENAME LAYER
    # -----------------------------

    def rename_layer(self, index, new_name):

        if not 0 <= index < len(self.layers):
            return False

        if not str(new_name).strip():
            return False

        self.layers[index]["name"] = str(new_name).strip()

        return True

    # -----------------------------
    # SHOW / HIDE LAYER
    # -----------------------------

    def set_visibility(self, index, visible):

        if not 0 <= index < len(self.layers):
            return False

        self.layers[index]["visible"] = bool(visible)

        return True

    # -----------------------------
    # SET OPACITY
    # -----------------------------

    def set_opacity(self, index, opacity):

        if not 0 <= index < len(self.layers):
            return False

        opacity = max(0.0, min(1.0, float(opacity)))

        self.layers[index]["opacity"] = opacity

        return True

    # -----------------------------
    # CLEAR LAYER
    # -----------------------------

    def clear_layer(self, index=None):

        if index is None:
            index = self.active_index

        if not 0 <= index < len(self.layers):
            return False

        self.layers[index]["canvas"].fill(0)

        return True

    # -----------------------------
    # COMBINE ALL LAYERS
    # -----------------------------

    def get_composite(self):

        composite = np.zeros(
            (self.height, self.width, 3),
            dtype=np.uint8
        )

        for layer in self.layers:

            if not layer["visible"]:
                continue

            opacity = layer["opacity"]

            layer_image = (
                layer["canvas"].astype(np.float32) * opacity
            ).astype(np.uint8)

            composite = np.clip(
                composite.astype(np.uint16)
                + layer_image.astype(np.uint16),
                0,
                255
            ).astype(np.uint8)

        return composite

    # -----------------------------
    # GET LAYER INFORMATION
    # -----------------------------

    def get_layers_info(self):

        result = []

        for index, layer in enumerate(self.layers):

            result.append({
                "index": index,
                "name": layer["name"],
                "visible": layer["visible"],
                "opacity": layer["opacity"],
                "active": index == self.active_index
            })

        return result