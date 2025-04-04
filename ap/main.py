from machine import Pin
import network
import time
import socket

led = Pin(2,Pin.OUT)

AP_SSID = "ESP32-C3-AP"
AP_PASSWORD = "12345678"
AP_CHANNEL = 6
AP_MAX_CONN = 4  # 确保固件支持此参数

def create_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    
    # 分步配置参数（避免未知参数）
    ap.config(essid=AP_SSID, password=AP_PASSWORD)
    ap.config(authmode=3)  # WPA2-PSK
    ap.config(channel=AP_CHANNEL)
    
    # 仅在新版本中添加 max_clients
    # ap.config(max_clients=AP_MAX_CONN)
    
    while not ap.active():
        print("等待热点启动...")
        time.sleep(1)
    print("热点已启动！IP:", ap.ifconfig()[0])

create_ap()

'''
# 动态显示连接设备
def list_connected_devices():
    ap = network.WLAN(network.AP_IF)
    stations = ap.status("stations")  # 获取连接设备列表
    print("已连接设备:", len(stations))
    for mac in stations:
        print("设备MAC地址:", mac)

# 每隔5秒扫描一次
while True:
    list_connected_devices()
    time.sleep(5)
'''

def start_http_server():
    ap_ip = network.WLAN(network.AP_IF).ifconfig()[0]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ap_ip, 80))
    s.listen(1)
    print("HTTP 服务器已启动:", ap_ip)
    
    while True:
        conn, addr = s.accept()
        request = conn.recv(1024)
        print("请求来自:", addr)
        response = "<html><meta charset='UTF-8'><head><title>ESP32网页控制界面(AP模式)</title><meta name='viewport'content='width=device-width, initial-scale=1'><link rel='icon'href='data:,'><style>html{font-family:Helvetica;display:inline-block;margin:0px auto;text-align:center}h1{color:#0F3376;padding:2vh}p{font-size:1.5rem}.button{display:inline-block;background-color:#e7bd3b;border:none;border-radius:4px;color:white;padding:16px 40px;text-decoration:none;font-size:30px;margin:2px;cursor:pointer}.button2{background-color:#4286f4}</style></head><body><p><a href='/?led=on'><button class='button'>ON</button></a></p><p><a href='/?led=off'><button class='button button2'>OFF</button></a></p></body></html>"
        conn.send(response)
        conn.close()
        
        res = str(request)
        led_on = res.find('/?led=on')
        led_off = res.find('/?led=off')
        if led_on == 6:
            print('LED ON')
            led.value(1)
            
        if led_off == 6:
            print('LED OFF')
            led.value(0)
               
start_http_server()
