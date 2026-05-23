import time
from inventor import Inventor, MOTOR_A, MOTOR_B
from pimoroni import REVERSED_DIR

# Settings
GEAR_RATIO = 50
BASE_SPEED = 0.4
SLEEP = 0.1
CORRECTION_GAIN = 0.2     # How strongly to correct speed differences

board = Inventor(motor_gear_ratio=GEAR_RATIO)

# Reverse left motor + encoder so forward means forward
board.motors[MOTOR_A].direction(REVERSED_DIR)
board.encoders[MOTOR_A].direction(REVERSED_DIR)

# Start both motors at the same base speed
left_speed = BASE_SPEED
right_speed = BASE_SPEED

board.motors[MOTOR_A].speed(left_speed)
board.motors[MOTOR_B].speed(right_speed)

try:
    while not board.switch_pressed():

        # Read encoder speeds
        left = board.encoders[MOTOR_A].capture().revolutions_per_second
        right = board.encoders[MOTOR_B].capture().revolutions_per_second

        print(f"LEFT={left:.3f}, RIGHT={right:.3f}")

        # Compute difference
        error = left - right

        # Apply correction
        left_speed  -= error * CORRECTION_GAIN
        right_speed += error * CORRECTION_GAIN

        # Clamp speeds to [-1, 1]
        left_speed = max(min(left_speed, 1.0), -1.0)
        right_speed = max(min(right_speed, 1.0), -1.0)

        # Update motors
        board.motors[MOTOR_A].speed(left_speed)
        board.motors[MOTOR_B].speed(right_speed)

        time.sleep(SLEEP)

finally:
    for m in board.motors:
        m.disable()
