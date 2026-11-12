"""
PhantomDraw AI
History Manager

Handles Undo and Redo operations
for the drawing canvas.
"""

import numpy as np


class HistoryManager:

    def __init__(self, max_history=30):

        self.max_history = max_history

        self.undo_stack = []
        self.redo_stack = []

    def save_state(self, canvas):
        """Save current canvas state."""

        self.undo_stack.append(canvas.copy())

        # Limit history size
        if len(self.undo_stack) > self.max_history:

            self.undo_stack.pop(0)

        # New drawing clears redo history
        self.redo_stack.clear()

    def undo(self, current_canvas):
        """Restore previous canvas state."""

        if not self.undo_stack:
            return current_canvas

        self.redo_stack.append(
            current_canvas.copy()
        )

        previous_canvas = self.undo_stack.pop()

        return previous_canvas.copy()

    def redo(self, current_canvas):
        """Restore previously undone canvas state."""

        if not self.redo_stack:
            return current_canvas

        self.undo_stack.append(
            current_canvas.copy()
        )

        next_canvas = self.redo_stack.pop()

        return next_canvas.copy()

    def clear_history(self):
        """Clear all saved history."""

        self.undo_stack.clear()
        self.redo_stack.clear()

    def can_undo(self):
        return len(self.undo_stack) > 0

    def can_redo(self):
        return len(self.redo_stack) > 0

    def get_history_info(self):

        return {
            "undo_available": self.can_undo(),
            "redo_available": self.can_redo(),
            "undo_count": len(self.undo_stack),
            "redo_count": len(self.redo_stack)
        }
        