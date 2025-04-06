from machine import I2S
from machine import Pin
 
# 初始化引脚定义
din_pin = Pin(2)
blck_pin = Pin(3)
lrc_pin = Pin(10)
 
 
# 初始化i2s
audio_out = I2S(0, sck=blck_pin, ws=lrc_pin, sd=din_pin, mode=I2S.TX, bits=16, format=I2S.MONO, rate=44100, ibuf=20000)
  
wavtempfile = "test.wav"
with open(wavtempfile,'rb') as f:
 
    # 跳过文件的开头的44个字节，直到数据段的第1个字节
    pos = f.seek(44) 
 
    # 用于减少while循环中堆分配的内存视图
    wav_samples = bytearray(1024)
    wav_samples_mv = memoryview(wav_samples)
     
    print("开始播放音频...")
    
    #并将其写入I2S DAC
    while True:
        try:
            num_read = f.readinto(wav_samples_mv)
            
            # WAV文件结束
            if num_read == 0: 
                break
 
            # 直到所有样本都写入I2S外围设备
            num_written = 0
            while num_written < num_read:
                num_written += audio_out.write(wav_samples_mv[num_written:num_read])
                
        except Exception as ret:
            print("产生异常...", ret)
            break