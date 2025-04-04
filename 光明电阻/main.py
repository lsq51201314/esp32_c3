import machine
import time

# 初始化ADC引脚 (根据实际连接调整引脚号)
adc = machine.ADC(machine.Pin(2))
adc.atten(machine.ADC.ATTN_11DB)  # 设置量程为 0-3.3V

def read_light():
    raw_value = adc.read()        # 读取原始ADC值 (0-4095)
    voltage = raw_value * 3.3 / 4095  # 转换为电压值
    
    #R_fixed = 10000  # 固定电阻10kΩ
    #R_ldr = R_fixed * (3.3 - voltage) / voltage  # 计算光敏电阻阻值
    #print(R_ldr)
    
    return raw_value, voltage

while True:
    raw, vol = read_light()
    print(f"ADC原始值: {raw} 电压: {vol:.2f}V")
    time.sleep(0.5)