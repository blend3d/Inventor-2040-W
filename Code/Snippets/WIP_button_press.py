from inventor import Inventor, MOTOR_A, MOTOR_B

board = Inventor()

# print("Press USER button to start...")
# 
# # Wait here until the button is pressed
# while not board.switch_pressed():	
#     pass
# 
# print("Starting main program!")
# 
# # --- Your main code here ---
# print("Press USER button to start...")
# 
# # Wait here until the button is pressed
# while not board.switch_pressed():	
#     pass

#help(Inventor)
print(board.switch_pressed())   # Note the parentheses
capture = board.encoders[MOTOR_A].capture()
help(board.encoders[MOTOR_A].capture())
print(board.encoder_a.capture())