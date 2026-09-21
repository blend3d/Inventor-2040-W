# ------------------------------
# Simplest straight‑line correction loop
# Uses the minimum added logic to keep the robot straight
# Does not use PID (proportional–integral–derivative) code
# No complicated math, just proportional correction
# Works well for SMARS + N20 motors
# 
# The table and plot in Thonny shows the motors being 
# corrected to have similar speeds 
# ------------------------------

import time
from inventor import Inventor, MOTOR_A, MOTOR_B
from pimoroni import REVERSED_DIR

# Wheel friendly names
LEFT = MOTOR_A
RIGHT = MOTOR_B
NAMES = ["LEFT", "RIGHT"]

# Settings
GEAR_RATIO = 50             # Gear ratio of the Pimoroni motors
SPEED_SCALE = 1.2           # Scaling to match real-world speeds
BASE_SPEED = 0.50			# Motor speed at 40%
SLEEP = 0.1					# 0.1 sec (100 ms)
CORRECTION_GAIN = 0.175    	# How strongly to correct speed differences

# ------------------------------
# Initialize motors
# ------------------------------
board = Inventor(motor_gear_ratio=GEAR_RATIO)

# Set the speed scale of the motors
board.motors[LEFT].speed_scale(SPEED_SCALE)
board.motors[RIGHT].speed_scale(SPEED_SCALE)

# Reverse left motor + encoder so forward moves SMARS forward
board.motors[LEFT].direction(REVERSED_DIR)
board.encoders[LEFT].direction(REVERSED_DIR)

# Start both motors at the same base speed
left_speed = BASE_SPEED
right_speed = BASE_SPEED

board.motors[LEFT].speed(left_speed)
board.motors[RIGHT].speed(right_speed)

# ------------------------------
# Wrap the code in a try block, to catch any exceptions 
# (including KeyboardInterrupt)
# ------------------------------
try:
    # Run the motors until the user button is pressed
    while not board.switch_pressed():

        # Read encoder speeds
        left = board.encoders[LEFT].capture().revolutions_per_second
        right = board.encoders[RIGHT].capture().revolutions_per_second

        print(f"LEFT = {left:.2f}   RIGHT = {right:.2f}   DELTA = {left-right:.2f}")
        
        # Compute difference
        error = left - right

        # Apply correction
        left_speed  -= error * CORRECTION_GAIN
        right_speed += error * CORRECTION_GAIN

        # Clamp speeds to [-1, 1]
        left_speed = max(min(left_speed, 1.0), -1.0)
        right_speed = max(min(right_speed, 1.0), -1.0)

        # Update motors
        board.motors[LEFT].speed(left_speed)
        board.motors[RIGHT].speed(right_speed)

        time.sleep(SLEEP)

# ------------------------------
# Put the board back into a safe state, regardless of how the program may have ended
# ------------------------------
finally:
    # Loop through all motors and disable
    for m in board.motors:
        m.disable()
