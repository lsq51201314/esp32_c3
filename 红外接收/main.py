import machine
import utime
from machine import Pin


class IR(object):

    CODE = {
        162: "电源", 226: "菜单",
        224: "音量+",144: "音量-",
        34: "上一曲", 194: "下一曲",2: "暂停",
        98: "向上", 168: "向下",
        104: "按键1", 152: "按键2", 176: "按键3",48: "按键4", 24: "按键5", 122: "按键6",16: "按键7", 56: "按键8", 90: "按键9",66: "按键0",
        82: "删除"
    }

    def __init__(self, gpioNum):
        self.irRecv = machine.Pin(gpioNum, machine.Pin.IN, machine.Pin.PULL_UP)
        self.irRecv.irq(trigger=machine.Pin.IRQ_RISING | machine.Pin.IRQ_FALLING, handler=self.__handler)  # 配置中断信息
        self.ir_step = 0
        self.ir_count = 0
        self.buf64 = [0 for i in range(64)]
        self.recived_ok = False
        self.cmd = None
        self.cmd_last = None
        self.repeat = 0
        self.repeat_last = None
        self.t_ok = None
        self.t_ok_last = None
        self.start = 0
        self.start_last = 0        
        self.changed = False

    def __handler(self, source):
        """
        中断回调函数
        """
        thisComeInTime = utime.ticks_us()

        # 更新时间
        curtime = utime.ticks_diff(thisComeInTime, self.start)
        self.start = thisComeInTime
        

        if curtime >= 8500 and curtime <= 9500:
            self.ir_step = 1
            return

        if self.ir_step == 1:
            if curtime >= 4000 and curtime <= 5000:
                self.ir_step = 2
                self.recived_ok = False
                self.ir_count = 0
                self.repeat = 0
            elif curtime >= 2000 and curtime <= 3000:  # 长按重复接收
                self.ir_step = 3
                self.repeat += 1

        elif self.ir_step == 2:  # 接收4个字节
            self.buf64[self.ir_count] = curtime
            self.ir_count += 1
            if self.ir_count >= 64:
                self.recived_ok = True
                self.t_ok = self.start #记录最后ok的时间
                self.ir_step = 0

        elif self.ir_step == 3:  # 重复
            if curtime >= 500 and curtime <= 650:
                self.repeat += 1

    def __check_cmd(self):
        byte4 = 0
        for i in range(32):
            x = i * 2
            t = self.buf64[x] + self.buf64[x+1]
            byte4 <<= 1
            if t >= 1800 and t <= 2800:
                byte4 += 1
        user_code_hi = (byte4 & 0xff000000) >> 24
        user_code_lo = (byte4 & 0x00ff0000) >> 16
        data_code = (byte4 & 0x0000ff00) >> 8
        data_code_r = byte4 & 0x000000ff
        self.cmd = data_code

    def scan(self):        
        # 接收到数据
        if self.recived_ok:
            self.__check_cmd()
            self.recived_ok = False
            
        # 数据有变化
        if self.cmd != self.cmd_last or self.repeat != self.repeat_last or self.t_ok != self.t_ok_last:
            self.changed = True
        else:
            self.changed = False

        # 更新
        self.cmd_last = self.cmd
        self.repeat_last = self.repeat
        self.t_ok_last = self.t_ok
        # 对应按钮字符
        # print(self.cmd)
        s = self.CODE.get(self.cmd)
        return self.changed, s, self.repeat, self.t_ok



if __name__ == "__main__":
    t = IR(2)
    while(True):
        changed, s, repeat, t_ok = t.scan()
        if changed and repeat>0:
            # print(changed, s, repeat, t_ok)
            print(s, repeat)
        
        