from machine import I2C, Pin
from vl53l1x import VL53L1X # library from: https://github.com/drakxtwo/vl53l1x_pico
import time

# -----------------------------
# I2C Setup (Inventor 2040 default pins)
# -----------------------------
i2c = I2C(0, scl=Pin(5), sda=Pin(4), freq=400000)

# -----------------------------
# Sensor Init
# -----------------------------
tof = VL53L1X(i2c)


print("\nVL53L1X Time‑of‑Flight Sensor Ready\n")

# -----------------------------
# Main Loop
# -----------------------------
while True:
    distance_mm = tof.read()
    print("Range: {:>4} mm".format(distance_mm))
    time.sleep(0.2)
