import dht
import machine
import time

# 初始化 DHT11，连接至 GPIO2
d = dht.DHT11(machine.Pin(2))

def read_sensor():
    try:
        d.measure()  # 启动传感器测量
        temp = d.temperature()  # 温度（单位：℃）
        humi = d.humidity()     # 湿度（单位：%）
        return temp, humi
    except Exception as e:
        print("读取失败:", e)
        return None, None

while True:
    temp, humi = read_sensor()
    if temp is not None and humi is not None:
        print(f"温度: {temp}℃, 湿度: {humi}%")
    else:
        print("传感器未响应！")
    time.sleep(2)  # DHT11 需至少 1 秒间隔