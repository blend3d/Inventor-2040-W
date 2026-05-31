from inventor import Inventor	# Loads Pimoroni’s Inventor 2040W helper class
import machine
import time

board = Inventor()				# Creates an object representing the Inventor 2040W board
led = machine.Pin("LED", machine.Pin.OUT)
                                # turn it on/off with led.value(1) or led.value(0)

print("Button test running... Press and release USER repeatedly.")

last_state = False   			# Track previous button state

while True:
    pressed = board.switch_pressed()	# Returns True when pressed, False when released
    
    # ----------------------------    
    # Only react when the state CHANGES
    # This prevents spammy output like:
    # Button Down
    # Button Down
    # Button Down
    # ----------------------------
    
    if pressed != last_state:	# If the button changed (up → down or down → up), then react
        last_state = pressed	# Update last_state so the next loop knows what the previous value was

        if pressed:				# If pressed returns True 
            led.value(1)
            print("Button Down")
        else:					# pressed returned False
            led.value(0)
            print("Button Up")

    time.sleep(0.02)   			# 20ms debounce to avoid jitter
