import machine
import os
import sdcard
# 大的模块需要5v供电
# 初始化SPI和SD卡（确认硬件支持8MHz）# 必须为8MHz（8000000）
spi = machine.SPI(1,baudrate=8000000,  sck=machine.Pin(10),mosi=machine.Pin(3),miso=machine.Pin(2))
cs = machine.Pin(6, machine.Pin.OUT)
sd = sdcard.SDCard(spi, cs)
os.mount(sd, '/sd')

# 递归遍历目录
def list_files(start_path):
    # 强制路径为字节类型
    if isinstance(start_path, str):
        start_path = start_path.encode('utf-8')
    
    for entry in os.listdir(start_path):
        # 确保entry为字节类型后再拼接
        if isinstance(entry, str):
            entry = entry.encode('utf-8')  # 兼容返回str的MicroPython版本
            
        full_path = start_path + '/' + entry
        stat = os.stat(full_path)  # 直接传递字节路径
        
        if stat[0] & 0x8000:
            print("文件:", full_path)
        else:
            print("目录:", full_path)
            list_files(full_path)  # 递归传递字节路径

# 初始调用使用字节路径
list_files('/sd')
 
# 卸载SD卡
os.umount('/sd')