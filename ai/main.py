 
 
 
class myWifiSet:
    def __init__(self) :
        self.Mode          =""
        self.APList        ={}#保存热点扫描结果
        #先尝试进入STA模式，连接热点，如果出错，就进入STA和AP混合模式
        if self.StaMode()==False:
            self.APMode()
            print("连接热点失败，进入STA&AP混合模式...")
            self.Mode="Hybrid"
        else:
            print("已进入STA模式，连接热点成功!")
            self.Mode="STA"
            
    def scanAP(self):
        #此方法只能在本类实例化后才能调用，即wifi变量已存在
        import utime,ujson
        #try:
        #    self.wifi.scan()#先尝试一次扫描
        #except:
        #    pass
        print("now in %s mode"%self.Mode)
        #self.wifi.active(False)#启停一次，确保扫描成功
        #utime.sleep(0.5)
        #self.wifi.active(True)
        #utime.sleep(0.5)
        #有时模块会读不出来信号弱的路由器名，因此写一段把名字为空的热点全部干掉！
        try:
            self.APList=self.wifi.scan()
            print("扫描AP结束，列表如下:")
            print(self.APList)
            f=open("/wifiAPList.json","w")
            #print(APList_json)
            for item in self.APList:
                print(item)
                if item[0]==b'':
                    print("one item deleted!")
                    self.APList.remove(item)
            for item in self.APList:
                print(item)
                if item[0]==b'':
                    print("one item deleted!")
                    self.APList.remove(item)
            APList_json=ujson.dumps(self.APList)
            f.write(APList_json)
            f.flush()
            f.close()
        except Exception as e:
            print("扫描AP错误:%s"%str(e))
 
    def StaMode(self):
        import json,utime,network
        try:
            with open('/wificonfig.json','r') as f:
                config = json.loads(f.read())
        # 若初次运行,则将进入excpet     
        except:
            print('WIFI配置文件错误!')
            return False
        #以下为正常的WIFI连接流程        
        self.wifi = network.WLAN(network.STA_IF)
        self.wifi.active(True)
        utime.sleep(0.5)
 
        if not self.wifi.isconnected(): 
            print('正在连接到热点%s...'%config['wifiname'])
            self.wifi.active(True)
            self.wifi.connect(config['wifiname'], config['wifipassword']) 
            import utime
 
            for i in range(10):
                print('第{}次尝试连接WIFI热点'.format(i+1))
                if self.wifi.isconnected():
                    break
                utime.sleep(2) #一般睡个5-10秒,应该绰绰有余
            
            if not self.wifi.isconnected():
                return False
            else:
                print('network config:',self.wifi.ifconfig())
                return True
        else:
            print('network config:', self.wifi.ifconfig())
            return True
            
    def APMode(self):
        #此方法为重点
        import utime,network
        try:
            if self.wifi.status()==network.STAT_CONNECTING:
                #变量wifi不存在的话，也会进入except
                print("强制退出STAT_CONNECTING状态...")
                #要想进入混合模式，就先进STA模式。
                #进入STA模式后，如果连接路由器失败，会一直停留在STA_CONNECTING状态
                #因此，先active(False)强制退出STA_CONNECTING状态，再active(True)回到STA初始状态
                #这样会避免后面scan()出现STA_CONNECTING状态禁止扫描的问题，同时也能进入混合模式
                self.wifi.active(False)
                self.wifi.active(True)
        except:
            pass
        self.wifi=network.WLAN(network.AP_IF)
        self.wifi.active(False)
        self.wifi.active(True)
        
#以下为测试代码
if __name__ == "__main__":
    import network
    #初始化时直接尝试进入STA模式连接热点，连接出错时进入STA与AP混合模式
    x=myWifiSet()
    if x.Mode=="STA":
        print("11111")
    elif x.Mode=="Hybrid":
        print("22222")
    #尝试扫描AP。不管在STA还是STA与AP混合模式，均可用以下方法正确扫描周围的AP列表
    x.scanAP()
    print(x.APList)
    
 