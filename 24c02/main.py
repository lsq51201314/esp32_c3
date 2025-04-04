from machine import I2C, Pin
import time

i2c = I2C(0, scl=Pin(2), sda=Pin(3), freq=400_000)  # 初始化I2C0，速率400kHz

def write_24c02(mem_address, data):
    # 将数据写入指定地址（单次写入最多8字节）
    if isinstance(data, int):
        data = bytes([data])
    elif isinstance(data, list):
        data = bytes(data)
    
    # 24C02的地址格式：高4位固定为1010，低3位由A0/A1/A2决定（全接地则为0）
    i2c.writeto(0x50, bytes([mem_address]) + data)  # 0x50是7位地址

def read_24c02(mem_address, length=1):
    # 从指定地址读取数据
    i2c.writeto(0x50, bytes([mem_address]), False)  # 发送地址
    return i2c.readfrom(0x50, length)               # 读取数据

def write_page(mem_address, data):
    page_size = 8  # 24C02的页大小
    for i in range(0, len(data), page_size):
        start = mem_address + i
        chunk = data[i:i+page_size]
        write_24c02(start, chunk)
        time.sleep_ms(5)  # 等待EEPROM写入完成
        
# 写入数据
data_to_write = b"这是一段存储测试的字符串内容，现在被写入到了芯片！0123456789abcdefghijklmnopqr+_)(*&^%$#@!~ABCDEFGHIJKLMNOPQRSTUVWXYZ"
write_page(0x00, data_to_write)

# 读取数据
read_data = read_24c02(0x00, len(data_to_write))
print("Read Data:", read_data.decode())