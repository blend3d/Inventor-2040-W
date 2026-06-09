# ------------------------------
# Using the USER button as a start/stop toggle for your SMARS robot
#
# Simplest straight‑line correction loop
# Uses the minimum added logic to keep the robot straight
# Does not use PID (proportional–integral–derivative) code
# No complicated math, just proportional correction
# Works well for SMARS + N20 motors
# 
# The table and plot shows the motors being corrected to have similar speeds 
# ------------------------------

from inventor import Inventor, MOTOR_A, MOTOR_B
from pimoroni import REVERSED_DIR
import machine
import time

# -----------------------------
# Settings for motors
# -----------------------------
GEAR_RATIO = 50
BASE_SPEED = 0.4			# Motor speed at 40%
SLEEP = 0.1					# 0.1 sec (100 ms)
CORRECTION_GAIN = 0.2     	# How strongly to correct speed differences

board = Inventor(motor_gear_ratio=GEAR_RATIO)

# Reverse left motor + encoder so forward means forward
board.motors[MOTOR_A].direction(REVERSED_DIR)
board.encoders[MOTOR_A].direction(REVERSED_DIR)

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
