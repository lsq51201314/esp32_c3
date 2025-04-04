from machine import Pin
import time

led2 = Pin(2,Pin.OUT)
led3 = Pin(3,Pin.OUT)
led10 = Pin(10,Pin.OUT)

while True:
    led2.value(1)
    time.sleep_ms(500)
    led2.value(0)
    time.sleep_ms(500)
    
    led3.value(1)
    time.sleep_ms(500)
    led3.value(0)
    time.sleep_ms(500)    

    led10.value(1)
    time.sleep_ms(500)
    led10.value(0)
    time.sleep_ms(500)
