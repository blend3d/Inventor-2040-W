import time
from inventor import Inventor, MOTOR_A, MOTOR_B
from pimoroni import REVERSED_DIR

# Friendly names
NAMES = ["LEFT", "RIGHT"]

# Settings
GEAR_RATIO = 50
SPEED = 0.4			# Speed at 40%
SLEEP = 0.1

# Create board
board = Inventor(motor_gear_ratio=GEAR_RATIO)

# Reverse left motor + encoder so forward means forward
board.motors[MOTOR_A].direction(REVERSED_DIR)
board.encoders[MOTOR_A].direction(REVERSED_DIR)

# Start both motors
board.motors[MOTOR_A].speed(SPEED)
board.motors[MOTOR_B].speed(SPEED)

try:
    while not board.switch_pressed():

        # Read both encoders
        left = board.encoders[MOTOR_A].capture()
        right = board.encoders[MOTOR_B].capture()

        # Print speeds
        print(f"{NAMES[0]} = {left.revolutions_per_second:.3f}, "
              f"{NAMES[1]} = {right.revolutions_per_second:.3f}")

        time.sleep(SLEEP)

finally:
    # Stop motors safely
    for m in board.motors:
        m.disable()
