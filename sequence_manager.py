import tkinter as tk

class SequenceManager:

    def __init__(
        self, 
        root, 
        canvas, 
        text_item_id,
        invisible_color="magenta", 
        visible_color="white",
        auto_clear_seconds=30
    ):
        self.root = root
        self.canvas = canvas
        self.text_id = text_item_id
        self.invis_col = invisible_color
        self.vis_col = visible_color
        self.sequence = []
        self.visible_persistent = False
        self.auto_clear_seconds = auto_clear_seconds if auto_clear_seconds and auto_clear_seconds > 0 else None
        self._auto_clear_after_id = None

    # ---------------------------- Sequence manipulation methods

    def add(self, tile):
        self.sequence.append(tile)
        self._update_canvas_text()
        self._reset_auto_clear_timer()

    def clear(self):
        self.sequence = []
        self._update_canvas_text()
        if self.visible_persistent:
            self._set_visible(False)
        self._cancel_auto_clear_timer()

    def get_sequence_text(self):
        if not self.sequence:
            return "(empty)"
        return " → ".join(self.sequence)

    # ---------------------------------- Display and visibility control

    def _update_canvas_text(self):
        text = self.get_sequence_text()
        try:
            self.canvas.itemconfig(self.text_id, text=text)
        except Exception:
            pass

    def _set_visible(self, yes: bool):
        color = self.vis_col if yes else self.invis_col
        try:
            self.canvas.itemconfig(self.text_id, fill=color)
        except Exception:
            pass
        self.visible_persistent = yes

    def toggle_display(self):
        new_state = not self.visible_persistent
        self._set_visible(new_state)

    # --------------------------------- Auto-clear timer management 

    def _reset_auto_clear_timer(self):
        if not self.auto_clear_seconds:
            return
        self._cancel_auto_clear_timer()
        ms = int(self.auto_clear_seconds * 1000)
        self._auto_clear_after_id = self.root.after(ms, self._do_auto_clear)

    def _cancel_auto_clear_timer(self):
        if self._auto_clear_after_id is not None:
            try:
                self.root.after_cancel(self._auto_clear_after_id)
            except Exception:
                pass
            self._auto_clear_after_id = None

    def _do_auto_clear(self):
        self._auto_clear_after_id = None
        self.clear()
        print("Sequence automatically cleared due to timeout (auto-clear).")

    # ------------------------------ Momentary display utility

    def show_once_momentary(self, duration_ms=1500):
        self._set_visible(True)

        def hide():
            if not self.visible_persistent:
                self._set_visible(False)

        self.root.after(duration_ms, hide)
