from machine import Pin
import time

beep = Pin(2, Pin.OUT)

while True:
    beep.value(1)
    time.sleep(1)
    beep.value(0)
    time.sleep(1)
    