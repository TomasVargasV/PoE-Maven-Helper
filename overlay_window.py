import tkinter as tk
import win32gui
import win32con
import win32api

def make_clickthrough(hwnd):
    style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    ws_ex_noactivate = getattr(win32con, "WS_EX_NOACTIVATE", 0x08000000)
    new_style = style | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | ws_ex_noactivate
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_style)

def create_overlay_window(border_thickness=5, border_color="red"):
    root = tk.Tk()
    root.title("PoE Maven Helper")
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    transparent_color = "magenta"
    root.configure(bg=transparent_color)
    root.attributes("-transparentcolor", transparent_color)

    screen_w = win32api.GetSystemMetrics(0)
    screen_h = win32api.GetSystemMetrics(1)

    canvas = tk.Canvas(
        root, 
        width=screen_w, 
        height=screen_h,
        bg=transparent_color, 
        highlightthickness=0, 
        bd=0
    )
    canvas.place(x=0, y=0, relwidth=1.0, relheight=1.0)

    b = border_thickness
    canvas.create_rectangle(
        b//2, b//2, 
        screen_w - b//2, screen_h - b//2,
        outline=border_color, 
        width=border_thickness
    )

    text_id = canvas.create_text(
        screen_w//2, 
        int(screen_h * 0.85),  
        text="",
        fill=transparent_color,  
        font=("Arial", 28), 
        anchor="c"
    )

    root.update_idletasks()
    hwnd_root = win32gui.FindWindow(None, "PoE Maven Helper")
    win32gui.MoveWindow(hwnd_root, 0, 0, screen_w, screen_h, True)

    make_clickthrough(hwnd_root)

    try:
        canvas.update_idletasks()
        hwnd_canvas = canvas.winfo_id()
        style_c = win32gui.GetWindowLong(hwnd_canvas, win32con.GWL_EXSTYLE)
        style_c |= win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd_canvas, win32con.GWL_EXSTYLE, style_c)
    except Exception as e:
        print("Warning: Unable to apply WS_EX_TRANSPARENT to the canvas:", e)

    return root, canvas, text_id
