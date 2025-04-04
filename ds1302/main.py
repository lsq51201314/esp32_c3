from machine import Pin
import ds1302
import time

ds = ds1302.DS1302(clk=Pin(2),dio=Pin(3),cs=Pin(10))

#年、月、日、星期、时、分、秒
ds.date_time([2025, 3, 29, 6, 17, 21, 59]) # set datetime.

while True:
    print(ds.date_time()) # returns the current datetime.
    time.sleep(1)