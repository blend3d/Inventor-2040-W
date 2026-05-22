from inventor import Inventor2040W, NUM_LEDS
from machine import I2C
# from vl53l1x import VL53L1X
import time

board = Inventor2040W()

BRIGHTNESS = 0.2
UPDATES = 50
SPEED = 20

def led_test(cycles):
    global offset, SPEED, BRIGHTNESS, NUM_LEDS
    offset = 0.0
    print(f'NUM_LEDS:{NUM_LEDS}')
    
    for _ in range(1, cycles):
        offset += SPEED / 1000.0
        for i in range(NUM_LEDS):
            hue = float(i) / NUM_LEDS
            board.leds.set_hsv(i, hue+offset, 1.0, BRIGHTNESS)
        print(f'offset: {offset}')
        time.sleep_ms(1000 // UPDATES)
    # Turn off the LED bars
    board.leds.clear()
    
led_test(1000)