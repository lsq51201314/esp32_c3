import machine
import network
import usocket as socket
import utime
 
# 配置WiFi
SSID = 'HUAWEI-1B94YK'
PASSWORD = '66668888'

WS_PIN = 8
SCK_PIN = 4
SD_PIN = 5

SAMPLE_RATE = 16000  # 采样率，单位：Hz
SAMPLE_SIZE_IN_BITS = 16  # 采样位深度，单位：位
CHANNELS = 1  # 声道数
BUFFER_LENGTH_IN_BYTES = 4096  # 缓冲区长度

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)
 
while not wlan.isconnected():
    pass
 
print('WiFi connected', wlan.ifconfig())
 
# 配置I2S接口
i2s = machine.I2S(
    0,
    sck=machine.Pin(SCK_PIN),
    ws=machine.Pin(WS_PIN),
    sd=machine.Pin(SD_PIN),
    mode=machine.I2S.RX,
    bits=SAMPLE_SIZE_IN_BITS,
    format=machine.I2S.MONO if CHANNELS == 1 else machine.I2S.STEREO,
    rate=SAMPLE_RATE,
    ibuf=BUFFER_LENGTH_IN_BYTES
)
 
# 创建UDP套接字
addr = socket.getaddrinfo('0.0.0.0', 8888)[0][-1]
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(addr)
 
print("等待音频数据流...")
 
try:
    while True:
        buffer = bytearray(BUFFER_LENGTH_IN_BYTES)
        # 从I2S接口读取音频数据
        read_len = i2s.readinto(buffer)  # 假设buf是一个预先定义的bytearray
        if read_len:
            # 将音频数据转换为适合网络传输的格式（如果需要）
            # 在这个简单例子中，我们直接发送原始音频数据
            # 注意：UDP是面向数据报的协议，可能会丢失或重新排序数据包
            sock.sendto(buffer[:read_len], ('127.0.0.1', 22345))
        
        # 可以添加延时以避免过快的循环
        utime.sleep_ms(10)
 
except KeyboardInterrupt:
    print("程序被中断")
 
finally:
    # 清理资源
    i2s.deinit()
    sock.close()