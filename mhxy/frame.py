import pygetwindow


class Frame:
    window: pygetwindow.Win32Window
    left: int
    right: int
    top: int
    bottom: int

    def __init__(self, window: pygetwindow.Win32Window = None):
        self.window = window
        if window is not None:
            self.left = window.left
            self.right = window.right
            self.top = window.top
            self.bottom = window.bottom
