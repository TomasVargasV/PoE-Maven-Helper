from pynput import keyboard
import win32gui
from . import events

def start_listening(event_queue):
    def on_press(key):
        
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)

        if "Path of Exile" not in title:
            return

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
            print("Erro no listener de teclado:", e)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener

