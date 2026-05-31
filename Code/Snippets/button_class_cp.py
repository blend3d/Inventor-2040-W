from inventor import Inventor
import time

class ButtonHandler:
    def __init__(self, board, debounce_ms=20):
        self.board = board
        self.debounce = debounce_ms / 1000   # convert to seconds
        self.last_state = False
        self.last_time = time.ticks_ms()

        # Optional callbacks
        self.on_press = None
        self.on_release = None

    def update(self):
        """Call this repeatedly inside your main loop."""
        now = time.ticks_ms()

        # Debounce timing
        if time.ticks_diff(now, self.last_time) < self.debounce * 1000:
            return

        pressed = self.board.switch_pressed()

        # Detect state change
        if pressed != self.last_state:
            self.last_state = pressed
            self.last_time = now

            if pressed:
                if self.on_press:
                    self.on_press()
            else:
                if self.on_release:
                    self.on_release()
