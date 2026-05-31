from inventor import Inventor
import machine
import time

board = Inventor()
led = machine.Pin("LED", machine.Pin.OUT)

#---------------------------------
# Helper functions
#---------------------------------

def wait_for_press():
    """Wait until the button is pressed."""
    while not board.switch_pressed():
        time.sleep(0.02)   # debounce

def wait_for_release():
    """Wait until the button is released."""
    while board.switch_pressed():
        time.sleep(0.02)   # debounce

#---------------------------------
# Main program
#---------------------------------

print("Press USER to START...")

# --- WAIT FOR START PRESS ---
wait_for_press()
wait_for_release()

print("STARTING program...")
led.value(1)   # LED ON to show running

# --- RUN UNTIL STOP PRESS ---
while True:
    # Your robot code goes here
    # Example: blink slowly to show it's running
    led.toggle()
    time.sleep(0.5)

    # Check for stop press
    if board.switch_pressed():
        break

# --- WAIT FOR RELEASE (important) ---
wait_for_release()

print("STOPPING program...")
led.value(0)
