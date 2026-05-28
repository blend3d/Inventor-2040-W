from inventor import Inventor
import machine
import time

board = Inventor()
led = machine.Pin("LED", machine.Pin.OUT)

print("Button test running... Press and release USER repeatedly.")

last_state = False   # Track previous button state

while True:
    pressed = board.switch_pressed()

    # Only react when the state CHANGES
    if pressed != last_state:
        last_state = pressed

        if pressed:
            led.value(1)
            print("Button Down")
        else:
            led.value(0)
            print("Button Up")

    time.sleep(0.02)   # 20ms debounce
