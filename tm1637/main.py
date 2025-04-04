from machine import Pin
import tm1637
import time
 
smg = tm1637.TM1637(dio=Pin(2),clk=Pin(3))
 
while True:
    smg.show("    ") # 四个空格，清屏
    time.sleep(1)
    
    smg.hex(10)  #十六进制A
    time.sleep(1)
    
    smg.number(1234)  # 显示数字，范围0-9999
    time.sleep(1)
    
    smg.numbers(11,56,0) # 时间显示，传递2个数值，最后一位1是点亮0是灭
    time.sleep(1)
    
    smg.temperature(22) #温度显示
    time.sleep(1)
    
    smg.show("2  9") # 输入空格则不显示，可用于清屏
    time.sleep(1)
    
    smg.show("{}   ".format(8))
    time.sleep(1)
    
    smg.show(" %.2d"%6) #显示06
    time.sleep(1)
    
    smg.scroll("0123 4567 89")  #向左滚动显示
    time.sleep(1)
