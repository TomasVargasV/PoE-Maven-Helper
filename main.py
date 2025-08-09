import queue
import sys
from overlay_window import create_overlay_window
from key_listener import start_listening
from sequence_manager import SequenceManager

POLL_INTERVAL_MS = 40

def main():
    root, canvas, text_id = create_overlay_window(border_thickness=5, border_color="red")
    
    seq_mgr = SequenceManager(
        root, canvas, text_id,
        invisible_color="magenta",
        visible_color="white",
        auto_clear_seconds=7
    )

    event_q = queue.Queue()
    listener = start_listening(event_q)

    def poll_queue():
        try:
            while not event_q.empty():
                ev = event_q.get_nowait()
                if ev in ("left", "top", "right"):
                    seq_mgr.add(ev)
                    print("Added:", ev)
                elif ev == "show":
                    seq_mgr.toggle_display()
                elif ev == "clear":
                    seq_mgr.clear()
                    print("Sequence cleared")
        except Exception as e:
            print("Error processing event queue:", e)
        finally:
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
