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

        if time.ticks_diff(now, self.last_time) < self.debounce:
            return

        pressed = self.board.switch_pressed()

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
# SMARS Program Start/Stop Logic
# -----------------------------
board = Inventor()
led = machine.Pin("LED", machine.Pin.OUT)

running = False   # Robot starts in IDLE mode

button = ButtonHandler(board)

def handle_press():
    global running
    running = not running   # toggle state

    if running:
        led.value(1)
        print("▶ Robot STARTED")
    else:
        led.value(0)
        print("⏹ Robot STOPPED")
        stop_robot()

button.on_press = handle_press


# -----------------------------
# Your robot behavior
# -----------------------------
def run_robot():
    """Put your SMARS movement code here."""
    # Example placeholder:
    print("Robot is running...")
    # motors, PID loops, ToF checks, etc.


def stop_robot():
    """Stop motors, reset encoders, etc."""
    for m in board.motors:
        m.speed(0)
    print("Motors stopped.")


# -----------------------------
# Main Loop
# -----------------------------
print("Press USER to start/stop SMARS robot.")

while True:
    button.update()

    if running:
        run_robot()

    time.sleep(0.01)
