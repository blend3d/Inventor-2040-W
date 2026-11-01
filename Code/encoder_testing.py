import time
from pimoroni import PID, NORMAL_DIR, REVERSED_DIR
from inventor import Inventor, MOTOR_A

"""
Demo of how a motor with an encoder can be used as a rotary encoder.
Press "User" to exit the program.
"""

GEAR_RATIO = 50             # The gear ratio of the motor
DIRECTION = REVERSED_DIR	# The direction to spin the motor in. NORMAL_DIR (0), REVERSED_DIR (1)
SPEED_SCALE = 5.4           # The scaling to apply to the motor's speed to match its real-world speed

# Create a new Inventor object and get a motor and encoder from it
board = Inventor(motor_gear_ratio=GEAR_RATIO)
m = board.motors[MOTOR_A]
enc = board.encoders[MOTOR_A]

# Set the motor and encoder's direction
m.direction(DIRECTION)
enc.direction(DIRECTION)

# Capture the state of the encoder and print initial state
capture = enc.capture()
print("\nInitial Encoder State")
print("Count:       ", capture.count)
print("Degrees:     ", capture.degrees)
print("Revolutions: ", capture.revolutions)

# Wrap the code in a try block, to catch any exceptions (including KeyboardInterrupt)
try:
    
    # Continually move the motor until the user button is pressed
    while not board.switch_pressed():

        # Capture the state of the encoder
        capture = enc.capture()
        test_count = capture.count
        time.sleep(0.1)
        
        # Capture the state of the encoder after a 0.1 sec delay
        capture = enc.capture()
        test_count_2 = capture.count
        
        # Check if the motor has moved, print encoder state if it has moved
        if test_count != test_count_2:
            print("\nCount:       ", capture.count)
            print("Count Delta: ", capture.delta)
            print("Degrees:     %6.4f" %capture.degrees)
            print("Revolutions: %4.4f" %capture.revolutions)
            # May be useful to determine rate of turn:
            # print("Deg per sec: ", capture.degrees_per_second) 
      
# Put the board back into a safe state when program ends
finally:
    # Disable the motor
    m.disable()

