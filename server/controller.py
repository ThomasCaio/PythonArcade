class Controller:
    def __init__(self):
        # Mouse Positioning in window.
        self.mouse_position = (0, 0)

        # MOVEMENT KEYS

        self.UP = 'W'
        self.LEFT = 'A'
        self.DOWN = 'S'
        self.RIGHT = 'D'

        # HOTKEYS

    def set_mouse_position(self, x, y):
        self.mouse_position = (x, y)
