from inventor import Inventor
import time

board = Inventor()

print("Press USER button to start...")

#---------------------------------
# Wait here until the button is pressed
#---------------------------------
while not board.switch_pressed():	
    # Run "pass" loop until the user button is pressed
    pass

# Exit "pass" loop, print message, and insert time delay for switch bounce to settle
print("USER button pressed, starting code...")
time.sleep(0.4)		# Time delay of 0.4 seconds

#---------------------------------
# Run code until the user button is pressed
#---------------------------------
try:
    # Run code until the user button is pressed
    while not board.switch_pressed():
        print(board.encoder_a.capture())

finally:
    # Run Code and Exit
    print("USER button pressed again, exiting program...")