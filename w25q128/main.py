from machine import SPI, Pin
import time
import uos

# 初始化SPI（模式0，频率20MHz）
spi = SPI(1, baudrate=20_000_000, sck=Pin(10), mosi=Pin(6), miso=Pin(3))
cs = Pin(2, Pin.OUT, value=1)  # 片选引脚初始高电平

class W25Q128:
    # 指令定义
    CMD_WRITE_ENABLE     = 0x06
    CMD_WRITE_DISABLE    = 0x04
    CMD_READ_DATA        = 0x03
    CMD_READ_STATUS_REG1 = 0x05
    CMD_PAGE_PROGRAM     = 0x02
    CMD_SECTOR_ERASE     = 0x20
    CMD_CHIP_ERASE       = 0xC7
    CMD_JEDEC_ID         = 0x9F

    def __init__(self, spi, cs):
        self.spi = spi
        self.cs = cs
        self._check_id()  # 验证芯片ID

    def _check_id(self):
        self.cs(0)
        self.spi.write(bytes([self.CMD_JEDEC_ID]))
        id_data = self.spi.read(3)
        self.cs(1)
        if id_data != b'\xef\x40\x18':  # W25Q128JV的JEDEC ID
            raise ValueError("Invalid Flash ID: {}".format(id_data))

    def _wait_busy(self):
        while True:
            self.cs(0)
            self.spi.write(bytes([self.CMD_READ_STATUS_REG1]))
            status = self.spi.read(1)[0]
            self.cs(1)
            if not (status & 0x01):  # 检查BUSY位
                break
            time.sleep_ms(1)

    def erase_sector(self, addr):
        self.cs(0)
        self.spi.write(bytes([self.CMD_WRITE_ENABLE]))
        self.cs(1)
        
        self.cs(0)
        cmd = bytes([self.CMD_SECTOR_ERASE, (addr >> 16) & 0xFF,
                    (addr >> 8) & 0xFF, addr & 0xFF])
        self.spi.write(cmd)
        self.cs(1)
        self._wait_busy()

    def write_page(self, addr, data):
        assert len(data) <= 256, "Page size exceeded"
        self.cs(0)
        self.spi.write(bytes([self.CMD_WRITE_ENABLE]))
        self.cs(1)
        
        self.cs(0)
        cmd = bytes([self.CMD_PAGE_PROGRAM, (addr >> 16) & 0xFF,
                    (addr >> 8) & 0xFF, addr & 0xFF])
        self.spi.write(cmd + data)
        self.cs(1)
        self._wait_busy()

    def read_data(self, addr, length):
        self.cs(0)
        cmd = bytes([self.CMD_READ_DATA, (addr >> 16) & 0xFF,
                    (addr >> 8) & 0xFF, addr & 0xFF])
        self.spi.write(cmd)
        data = self.spi.read(length)
        self.cs(1)
        return data

# 初始化Flash
flash = W25Q128(spi, cs)

'''
# 擦除第一个扇区（4KB）
flash.erase_sector(0x000000)

# 写入测试数据（页编程）
data_to_write = b"这是一段存储测试的字符串内容，现在被写入到了芯片！0123456789abcdefghijklmnopqr+_)(*&^%$#@!~ABCDEFGHIJKLMNOPQRSTUVWXYZ"
for i in range(0, len(data_to_write), 256):
    chunk = data_to_write[i:i+256]
    flash.write_page(i, chunk)

# 读取并验证数据
read_data = flash.read_data(0, len(data_to_write))
print("Read Data:", read_data[:len(data_to_write)].decode())
print("Verification:", "Success" if read_data == data_to_write else "Failed")
'''

'''
#固件存储
def update_firmware(new_bin_data):
    # 擦除目标区域（例如从1MB地址开始）
    for sector in range(0x100000, 0x100000 + len(new_bin_data), 4096):
        flash.erase_sector(sector)
    
    # 分页写入新固件
    for i in range(0, len(new_bin_data), 256):
        flash.write_page(0x100000 + i, new_bin_data[i:i+256])
'''

'''
#数据日志存储
LOG_START = 0x200000
current_addr = LOG_START

def log_sensor_data(data):
    global current_addr
    timestamp = time.time()
    entry = f"{timestamp},{data}\n".encode()
    
    # 检查剩余空间
    if current_addr + len(entry) > LOG_START + 1*1024*1024:
        current_addr = LOG_START  # 循环覆盖
    
    # 写入数据
    flash.write_page(current_addr, entry)
    current_addr += len(entry)        
'''  
  
#文件系统集成
class FlashBlockDev:
    ERASE_BLOCK_SIZE = 4096  # 4KB擦除单位
    READ_BLOCK_SIZE = 256    # 最小读取单位
    
    def __init__(self, flash, start_addr, size):
        self.flash = flash
        self.start = start_addr
        self.size = size
    
    def readblocks(self, block_num, buf):
        addr = self.start + block_num * self.ERASE_BLOCK_SIZE
        data = self.flash.read_data(addr, len(buf))
        buf[:] = data
    
    def writeblocks(self, block_num, buf):
        addr = self.start + block_num * self.ERASE_BLOCK_SIZE
        self.flash.erase_sector(addr)
        for i in range(0, len(buf), 256):
            self.flash.write_page(addr + i, buf[i:i+256])
    
    def ioctl(self, op, arg):
        if op == 4:  # BP_IOCTL_SEC_COUNT
            return self.size // self.ERASE_BLOCK_SIZE
        if op == 5:  # BP_IOCTL_SEC_SIZE
            return self.ERASE_BLOCK_SIZE

# 挂载前10MB为文件系统
block_dev = FlashBlockDev(flash, 0x100000, 10*1024*1024)
uos.VfsFat.mkfs(block_dev)  # 格式化（首次使用）
uos.mount(block_dev, "/flash")

# 使用示例
with open("/flash/test.txt", "w") as f:
    f.write("这是一段存储测试的字符串内容，现在被写入到了芯片！0123456789abcdefghijklmnopqr+_)(*&^%$#@!~ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    
    
print(open("/flash/test.txt").read())
