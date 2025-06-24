"""
cursor_highlighter.py

A script to highlight the mouse cursor with a red circle using hotkeys.
"""
# === Required Libraries ===

import pyautogui        # used to get the current mouse position
import tkinter as tk    # used to create a small transparent GUI window with a red circle
import threading        # used to run the highlight loop in a separate thread
import keyboard         # used to register hotkeys for starting/stopping the highlighter and quitting the app
import time             # used for a small delay in the loop to reduce CPU usage

class CursorHighlighter:
    """
    A class to visually highlight the mouse cursor using a red circle overlay.
    
    Methods:
    - start(): Enable the overlay and follow the mouse
    - stop(): Disable the overlay
    - show_status_window(): Display a notification window with usage instructions
    - hide_status_window(): Close the notification window
    """
    def __init__(self):
        """Initialize state and placeholders for GUI and threading."""
        self.running = False    # Whether the highlighter is currently active
        self.root = None        # Tkinter root window
        self.canvas = None      # Canvas inside the Tkinter window
        self.thread = None      # Thread running the highlight loop
        self.status_root = None # Status window with usage info

    def show_status_window(self):
        """
        Create a small, always-on-top status window with usage instructions.
        Styled like old-school developer tools for visual feedback.
        """
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

        # Position window
        screen_width = self.status_root.winfo_screenwidth()
        screen_height = self.status_root.winfo_screenheight()
        self.status_root.geometry(f"+{screen_width - 850}+{screen_height - 65}")

    def hide_status_window(self):
        """Close the status window if it exists."""
        if self.status_root:
            self.status_root.destroy()
            self.status_root = None

    def _highlight_loop(self):
        """
        Internal method: Runs in a separate thread to draw a red circle
        that follows the mouse cursor in real-time.
        """
        # Create transparent, borderless topmost window
        self.root = tk.Tk()
        self.root.attributes("-topmost", True)      # Always on top
        self.root.overrideredirect(True)            # No window decorations
        self.root.wm_attributes("-transparentcolor", "white")   # Make white color fully transparent
        self.root.configure(bg="white")             # Set background to transparent marker

        # Draw a red circle on a white canvas (white will be transparent)
        self.canvas = tk.Canvas(self.root, width=100, height=100, bg="white", highlightthickness=0)
        self.canvas.pack()
        self.canvas.create_oval(10, 10, 90, 90, outline="red", width=4)

        # Loop while the highlighter is active
        while self.running:
            x, y = pyautogui.position()
            self.root.geometry(f"100x100+{x - 50}+{y - 50}")
            self.root.update()
            time.sleep(0.01)

        # Cleanup after stopping
        self.root.destroy()
        self.root = None
        self.canvas = None

    def start(self):
        """Start the red circle overlay by launching the highlight loop in a new thread."""
        if not self.running:
            print("🔴 Highlighter ON (press F9 to turn OFF)")
            self.running = True
            self.thread = threading.Thread(target=self._highlight_loop, daemon=True)
            self.thread.start()

    def stop(self):
        """Stop the overlay and wait for the background thread to finish."""
        if self.running:
            print("⚪ Highlighter OFF (press F8 to turn ON)")
            self.running = False
            if self.thread:
                self.thread.join()
            self.thread = None

if __name__ == "__main__":
    # Create the highlighter controller object
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
