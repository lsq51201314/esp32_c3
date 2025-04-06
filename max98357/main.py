from machine import I2S,Pin
import urequests
import network
import time

# 初始化引脚定义
din_pin = Pin(2)
blck_pin = Pin(3)
lrc_pin = Pin(10)
  
# 初始化i2s
audio_out = I2S(0, sck=blck_pin, ws=lrc_pin, sd=din_pin, mode=I2S.TX, bits=16, format=I2S.MONO, rate=44100, ibuf=20000)
 
# 连接网络函数
def do_connect():
    """链接WIFI网络"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('HUAWEI-1B94YK', '66668888')  # WIFI名字密码
        i = 1
        while not wlan.isconnected():
            print("正在链接中...{}".format(i))
            i += 1
            time.sleep(1)
    print('network config:', wlan.ifconfig())
 
 
# 连接网络
do_connect()
 
# 注意不要用https,要用http
response = urequests.get("http://doc.itprojects.cn/0006.zhishi.esp32/01.download/audio/chaojimali.wav", stream=True)
response.raw.read(44)  # 跳过开头的44字节音频文件头信息
 
print("开始播放音频...")
 
#并将其写入I2S DAC
while True:
    try:
        content_byte = response.raw.read(1024)  # 每次读取1024个字节
        
        # 判断WAV文件是否结束
        if len(content_byte) == 0: 
            break
        # 调用I2S对象播放音频
        audio_out.write(content_byte) 
            
    except Exception as ret:
        print("程序产生异常...", ret)
        audio_out.deinit()
        break
 
audio_out.deinit()  # 音乐播放完毕后，退出