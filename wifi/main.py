import network
import time
import urequests

# 配置 Wi-Fi 信息
SSID = "HUAWEI-1B94YK"
PASSWORD = "66668888"

def connect_wifi():
    # 初始化 Wi-Fi 客户端模式
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)  # 激活 Wi-Fi
    
    if not wlan.isconnected():
        print("正在连接 Wi-Fi...")
        wlan.connect(SSID, PASSWORD)
        
        # 等待连接，最多 10 秒
        max_wait = 10
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            print("等待连接...", max_wait)
            time.sleep(1)
        
        if wlan.isconnected():
            print("连接成功！")
            print("IP 地址:", wlan.ifconfig()[0])
        else:
            print("连接失败！")
    
    return wlan

# 执行连接
wifi = connect_wifi()


'''
#自动重连机制
def auto_reconnect():
    import machine
    while True:
        if not wifi.isconnected():
            print("Wi-Fi 断开，尝试重连...")
            wifi.connect(SSID, PASSWORD)
            time.sleep(5)
            if not wifi.isconnected():
                print("重连失败，重启设备...")
                machine.reset()
        time.sleep(1)
'''


# GET请求
try:
    if wifi.isconnected():
        response = urequests.get("http://192.168.100.102:22345/api/esp32")
        print("状态码:", response.status_code)
        print("响应内容:", response.text)
        response.close()
    else:
        print("未连接 Wi-Fi！")
except Exception as e:
    print("请求失败:", e)


# POST请求
try:
    if wifi.isconnected():
        response = urequests.post("http://192.168.100.102:22345/api/esp32", json={"code": 200,"type": "POST"}, headers={"Content-Type": "application/json"})
        print("状态码:", response.status_code)
        print("响应内容:", response.text)
        response.close() 
    else:
        print("未连接 Wi-Fi！")
except Exception as e:
    print("请求失败:", e)
       