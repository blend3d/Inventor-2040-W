from inventor import Inventor

board = Inventor()

print("Press USER button to start...")

# Wait here until the button is pressed
while not board.switch_pressed():
    pass

print("Starting main program!")

# --- Your main code here ---