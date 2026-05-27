from inventor import Inventor
import time
import utime

board = Inventor()
led_onboard = machine.Pin("LED", machine.Pin.OUT)

print("Press USER button to start...")

#---------------------------------
# Wait here until the button is pressed
#---------------------------------
try:
    while not board.switch_pressed():	
        # Run "pass" loop until the user button is pressed
        led_onboard.value(1)
        pass

finally:
    # Exit "pass" loop, print message, and insert time delay for switch bounce to settle
    print("USER button pressed, starting code...")
    # time.sleep(0.4)		# Time delay of 0.4 seconds

#---------------------------------
# Run code until the user button is pressed
#---------------------------------
try:
    # Run code until the user button is pressed
    while not board.switch_pressed():
        led_onboard.value(1)
        utime.sleep(0.1)
        led_onboard.value(0)
        utime.sleep(1.75)

finally:
    # Run Code and Exit
    print("USER button pressed again, exiting program...")