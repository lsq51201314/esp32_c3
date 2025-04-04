import machine
import time
import math

# 初始化 AO（模拟输入）
adc = machine.ADC(machine.Pin(3))
adc.atten(machine.ADC.ATTN_11DB)  # 量程 0-3.3V

# 初始化 DO（数字输入，启用内部上拉电阻）
do_pin = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)

def read_ao(samples=100):
    # 采集模拟信号并计算有效值（RMS）
    values = [adc.read() for _ in range(samples)]
    offset = sum(values) / samples  # 计算直流偏移（静默基准）
    sum_sq = sum((v - offset)**2 for v in values)
    rms = math.sqrt(sum_sq / samples)
    return rms

def check_do():
    # 检测 DO 引脚状态（假设低电平表示触发）
    return do_pin.value() == 0

while True:
    # 读取 AO 模拟信号
    volume_rms = read_ao()
    voltage = volume_rms #* 3.3 / 4095  # 转换为电压
    #print(f"AO 音量强度: {volume_rms:.1f} 电压: {voltage:.2f}V")
    print(f"AO {volume_rms:.1f}")
    
    '''
    # 检测 DO 触发信号
    if check_do():
        print("DO 触发：检测到大声！")
    else:
        print("DO 未触发")
    '''
    
    time.sleep(0.1)