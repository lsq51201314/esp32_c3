from machine import Pin,PWM
import time

led = PWM(Pin(10))
led.freq(1000)

while True:
    for i in range(0,1023):
        led.duty(i)
        time.sleep_ms(1)
    for i in range(1023,0,-1):
        led.duty(i)
        time.sleep_ms(1)
