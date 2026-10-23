# ------------------------------ 
# Inventor 2040 W and 2350 W robot program.  
# blend3d@gmail.com 10/16/2026
# Press "USER" button to exit program.
# ------------------------------

from vl53l1x import VL53L1X # Library in lib folder
from machine import I2C, Pin
from inventor import Inventor, MOTOR_A, MOTOR_B, NUM_MOTORS
from pimoroni import REVERSED_DIR
import utime, sys

# User button set-up for use as an interrupt
stop_requested = False
User_sw = Pin(22, Pin.IN) 	# User button is pin GP22

# Robot "friendly" motor names
LEFT = MOTOR_A
RIGHT = MOTOR_B
NAMES = ["LEFT", "RIGHT"]   # Tuple for calling motors by [i] index

# Constants
GEAR_RATIO = 50				# Pimoroni's MMME gear ratio
SPEED_SCALE = 1.2           # Scaling to match real-world speeds
BASE_SPEED = 0.75			# 75% Motor speed 
SLEEP = 0.1					# 0.1 sec (100 ms)
MOTOR_CORRECTION = 1.1  	# Motor correction factor for motors running backwards at 75%
NEW_SPEED = BASE_SPEED		# Initialize NEW_SPEED equal to BASE_SPEED 
distance_trigger = 190      # More than 200 causes false stops

# ------------------------------
# Initialize Motors and TOF Distance Sensor
# ------------------------------

i2c = I2C(0)
distance = VL53L1X(i2c)

# Create an Inventor object
board = Inventor(motor_gear_ratio=GEAR_RATIO)

# Set the speed scale of the motors
board.motors[LEFT].speed_scale(SPEED_SCALE)
board.motors[RIGHT].speed_scale(SPEED_SCALE)

# Reverse the direction of the left motor and encoder for forward movement
board.motors[LEFT].direction(REVERSED_DIR)
board.encoders[LEFT].direction(REVERSED_DIR)

# ------------------------------
# Functions
# ------------------------------

def move_forward():
    """
    LH Correction added to to have robot move in less of an arc forward
    due to the LH motor running in reverse.
    """
    # Start both motors at the same base speed
    left_speed = BASE_SPEED
    right_speed = BASE_SPEED

    board.motors[LEFT].speed(left_speed * MOTOR_CORRECTION)
    board.motors[RIGHT].speed(right_speed)

def move_backward():
    """
    RH Correction added to to have robot move in less of an arc backward
    due to the RH motor running in reverse.      
    """
    # Start both motors at the same reverse base speed
    left_speed = -BASE_SPEED
    right_speed = -BASE_SPEED
      
    board.motors[LEFT].speed(left_speed)
    board.motors[RIGHT].speed(right_speed * MOTOR_CORRECTION)

def arc_right():
    """
    LH Correction added to to have robot move correctly in an right 
    handed arc forward due to the LH motor running in reverse.        
    """
    # Start motors at an approximate 1.5:1 left/right base speed
    left_speed = 1.25 * BASE_SPEED
    right_speed = 0.85 * BASE_SPEED
    
    board.motors[LEFT].speed(left_speed * MOTOR_CORRECTION)
    board.motors[RIGHT].speed(right_speed)

def tank_turn_right():
    """
    RH Tank turn, both motors are in reverse, no correction required.
    Turn time is based on observations for a 90 degree turn
    """
    left_speed = BASE_SPEED
    right_speed = -BASE_SPEED
    
    board.motors[LEFT].speed(left_speed)
    board.motors[RIGHT].speed(right_speed)

    utime.sleep(0.4)

def arc_left():
    """
    LH Correction added to to have robot move correctly in an left 
    handed arc forward due to the LH motor running in reverse.            
    """
    # Start motors at an approximate 1:1.5 left/right base speed
    left_speed = 0.85 * BASE_SPEED
    right_speed = 1.25 * BASE_SPEED
    
    board.motors[LEFT].speed(left_speed * MOTOR_CORRECTION)
    board.motors[RIGHT].speed(right_speed)

def tank_turn_left():
    """
    LH Tank turn. both motors are in forward, no correction required.
    Turn time is based on observations for a 90 degree turn
    """
    left_speed = -BASE_SPEED
    right_speed = BASE_SPEED
    
    board.motors[LEFT].speed(left_speed)
    board.motors[RIGHT].speed(right_speed)
    
    utime.sleep(0.45)
    
def brake_motors():
    """
    Similar to shorting the motor leads together which has the effect of
    braking the motor for a quick stop.		
    """
    board.motors[LEFT].brake()
    board.motors[RIGHT].brake()
    # Add 0.2 sec delay for a smooth transition between drive functions
    utime.sleep(0.2)
    
def coast_to_stop():
    """
    Coast to a stop with short delay
    """
    board.motors[LEFT].coast()
    board.motors[RIGHT].coast()
    # Add 0.4 sec delay for a smooth transition between drive functions
    utime.sleep(0.4)

def set_speed(set_speed = 0.5):
    # ***** WIP *****
    # Sets the new speed of the motors
    NEW_SPEED = set_speed    
    print("Motor speed set to " + str(NEW_SPEED) + "\n")

def user_sw_interrupt(pin):
    """
    # Interrupt service routine
    """
    global stop_requested
    print("\nInterrupt called\n")
    stop_requested = True
    print("Stop request =", stop_requested, "\n")
    
def scan():
    distance_scan = distance.read()
    print("range: mm ", distance.read())
    utime.sleep(0.05)
    return distance_scan

# Interrupt set-up to call service routine
User_sw.irq(handler=user_sw_interrupt, trigger=User_sw.IRQ_FALLING)

# Give user 5 seconds to power on battery and set SMARS down
utime.sleep(5)

# ------------------------------
# Main Program Loop
# ------------------------------

# Wrap the code in a try block, to catch any exceptions
try:
    # Enable the motors
    for m in board.motors:
        m.enable()
    print("SMARS motor are enabled.\n")

    # Continually run program until the user switch is pressed
    while True:
        if stop_requested:
            print("User interrupt detected, stopping program.")
            break
        
        # ------------------------------
        # Program loop for robot's behavior
        # ------------------------------
        
        # Assign scan() distance to distance_forward
        distance_forward = scan()
        
        # print function is for test only
        print("range: mm ", distance_forward)
         
        # Check to see if an obstacle is sensed
        if distance_forward < distance_trigger:             
            
            # If True (hazard detected) backup and turn 90 degrees right
            brake_motors()
            move_backward()                        
            utime.sleep(0.8)
            brake_motors()
            tank_turn_right()                           
            brake_motors()                             
            
            # Assign scan() distance to distance_right                                 
            distance_right = scan()                  
            
            # turn to the left 180 degrees to the left
            tank_turn_left()
            tank_turn_left()
            brake_motors()                                                       
            
            # Assign scan() distance to distance_left                             
            distance_left = scan()
            
            # If distance left is less than right, turn 180 deg right and move forward
            if(distance_left < distance_right):               
                tank_turn_right()
                tank_turn_right()
                brake_motors()
                move_forward()
            
            # If distance right is less than left, move forward
            else:
                move_forward()
                
        # if False (no hazards detected) continue forward
        else:
            move_forward() 

# Put board into a safe state upon exit
finally:
    
    # Stop the motors
    for m in board.motors:
        m.disable()
    print("\nMotors are disabled.\n")

