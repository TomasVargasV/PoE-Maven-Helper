from pynput import keyboard

def start_listening(event_queue):
    def on_press(key):
        try:
            if key == keyboard.Key.left:
                event_queue.put("left")
            elif key == keyboard.Key.up:
                event_queue.put("top")
            elif key == keyboard.Key.right:
                event_queue.put("right")
            elif key == keyboard.Key.enter:
                event_queue.put("show")
            elif key == keyboard.Key.esc:
                event_queue.put("clear")
        except Exception as e:
            print("Error in keyboard listener:", e)

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener
