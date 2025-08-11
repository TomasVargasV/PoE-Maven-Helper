from pynput import keyboard
from . import events

def start_listening(event_queue):
    def on_press(key):
        try:
            if key == keyboard.Key.left:
                event_queue.put(events.LEFT)
            elif key == keyboard.Key.up:
                event_queue.put(events.TOP)
            elif key == keyboard.Key.right:
                event_queue.put(events.RIGHT)
            elif key == keyboard.Key.enter:
                event_queue.put(events.SHOW)
            elif key == keyboard.Key.esc:
                event_queue.put(events.CLEAR)
        except Exception as e:
            print("Error in keyboard listener:", e)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener
