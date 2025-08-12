import queue
import sys
from core import Sequence, start_listening, events
from ui import create_overlay_window

POLL_INTERVAL_MS = 40

def main():
    root, display = create_overlay_window()

    sequence = Sequence(auto_clear_seconds=7)

    event_queue = queue.Queue()

    listener = start_listening(event_queue)

    display.update_text(sequence.get_sequence())
    display.toggle_display()

    def poll_queue():
        try:
            while not event_queue.empty():
                event = event_queue.get_nowait()
                if event in events.DIRECTIONS:
                    sequence.add(event)
                    display.update_text(sequence.get_sequence())
                elif event == events.SHOW:
                    display.toggle_display()
                elif event == events.CLEAR:
                    sequence.clear()
                    display.update_text(sequence.get_sequence())
        except Exception as e:
            print("Error processing event queue:", e)
        finally:
            if sequence.should_auto_clear():
                sequence.clear()
                display.update_text(sequence.get_sequence())
            root.after(POLL_INTERVAL_MS, poll_queue)

    root.after(POLL_INTERVAL_MS, poll_queue)
    def on_close():
        try:
            listener.stop()
        except Exception:
            pass
        root.destroy()
        sys.exit(0)

    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()

if __name__ == "__main__":
    main()