from inventor import Inventor
import machine
import time

# -----------------------------
# Button Handler Class
# -----------------------------
class ButtonHandler:
    def __init__(self, board, debounce_ms=20):
        self.board = board
        self.debounce = debounce_ms
        self.last_state = False
        self.last_time = time.ticks_ms()

        self.on_press = None
        self.on_release = None

    def update(self):
        now = time.ticks_ms()

        # Debounce check
        if time.ticks_diff(now, self.last_time) < self.debounce:
            return

        pressed = self.board.switch_pressed()

        # Detect change
        if pressed != self.last_state:
            self.last_state = pressed
            self.last_time = now

            if pressed:
                if self.on_press:
                    self.on_press()
            else:
                if self.on_release:
                    self.on_release()


# -----------------------------
# Main Program
# -----------------------------
board = Inventor()
led = machine.Pin("LED", machine.Pin.OUT)

button = ButtonHandler(board)

def handle_press():
    led.value(1)
    print("Button Down")

def handle_release():
    led.value(0)
    print("Button Up")

button.on_press = handle_press
button.on_release = handle_release

print("Class-based button handler running...")

while True:
    button.update()
    time.sleep(0.005)
