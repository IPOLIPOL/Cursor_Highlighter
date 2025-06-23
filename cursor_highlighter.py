import pyautogui
import tkinter as tk
import threading
import keyboard
import time

class CursorHighlighter:
    def __init__(self):
        self.running = False
        self.root = None
        self.canvas = None
        self.thread = None
        self.status_root = None  # New: status window

    def show_status_window(self):
        self.status_root = tk.Toplevel()
        self.status_root.overrideredirect(True)
        self.status_root.attributes("-topmost", True)
        self.status_root.configure(bg="#000080")  # Dark blue, classic

        frame = tk.Frame(self.status_root, bg="#000080", bd=2, relief="ridge")
        frame.pack()

        label = tk.Label(
            frame,
            text="✅ Ready. Press F8 to turn ON, F9 to turn OFF, ESC to quit.",
            bg="#000080",
            fg="yellow",  # Or cyan for Borland C-style
            font=("Courier New", 8, "bold"),  # Monospace
            justify="left"
        )
        label.pack(ipadx=6, ipady=3)

        # Position top-left or bottom-right like 80s layout
        screen_width = self.status_root.winfo_screenwidth()
        screen_height = self.status_root.winfo_screenheight()
        self.status_root.geometry(f"+{screen_width - 850}+{screen_height - 65}")

    def hide_status_window(self):
        if self.status_root:
            self.status_root.destroy()
            self.status_root = None

    def _highlight_loop(self):
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)
        self.root.overrideredirect(True)
        self.root.wm_attributes("-transparentcolor", "white")
        self.root.configure(bg="white")

        self.canvas = tk.Canvas(self.root, width=100, height=100, bg="white", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_oval(10, 10, 90, 90, outline="red", width=4)

        while self.running:
            x, y = pyautogui.position()
            self.root.geometry(f"100x100+{x - 50}+{y - 50}")
            self.root.update()
            time.sleep(0.01)

        self.root.destroy()
        self.root = None
        self.canvas = None

    def start(self):
        if not self.running:
            print("🔴 Highlighter ON (press F9 to turn OFF)")
            self.running = True
            self.thread = threading.Thread(target=self._highlight_loop, daemon=True)
            self.thread.start()

    def stop(self):
        if self.running:
            print("⚪ Highlighter OFF (press F8 to turn ON)")
            self.running = False
            if self.thread:
                self.thread.join()
            self.thread = None

if __name__ == "__main__":
    highlighter = CursorHighlighter()

    # Show on-screen message window
    main_ui = tk.Tk()
    main_ui.withdraw()  # Hide the main Tk window
    highlighter.show_status_window()

    # Register hotkeys
    keyboard.add_hotkey("f8", highlighter.start)
    keyboard.add_hotkey("f9", highlighter.stop)
    keyboard.add_hotkey("esc", lambda: (highlighter.stop(), highlighter.hide_status_window(), exit()))

    print("✅ Ready. Press F8 to turn ON, F9 to turn OFF, ESC to quit.")

    # Run background Tk loop for the status window
    main_ui.mainloop()
