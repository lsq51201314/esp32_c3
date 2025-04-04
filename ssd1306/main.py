from machine import SPI, Pin
from ssd1306 import SSD1306
import time
import ufont

D0 = Pin(2)  # SCK
D1 = Pin(3)  # MOSI
RES = Pin(10)
DC = Pin(6)
CS = Pin(7)

spi = SPI(1,baudrate=8000000, sck=D0, mosi=D1)
display = SSD1306(spi=spi, dc=DC, res=RES, cs=CS)
display.fill(0)

# 载入字体
font = ufont.BMFont("font.bmf")

'''
# 最简单的显示 "你好",其中指定 `show=True` 使得屏幕及时更新
font.text(display, "你好", 0, 0, show=True)
time.sleep(1)

# 如果想让文字显示在屏幕正中间，可以通过指定文本左上角位置来修改显示位置
font.text(display, "你好", 48, 16, show=True)
time.sleep(1)

# 此时你会发现：上一次显示显示的文字不会消失。因为你没有指定清屏参数：`clear=True`;让我们再试一次
# 注意，请使用修改后的 `ssd1306.py` 驱动，否则请自行调用`display.fill(0)`
font.text(display, "你好", 48, 16, show=True, clear=True)
time.sleep(1)

# 显示英文呢
font.text(display, "He110", 48, 8, show=True, clear=True)
font.text(display, "你好", 48, 24, show=True)
time.sleep(1)

# 会发现一个汉字的宽度大概是字母的两倍，如果你需要等宽，可以指定参数 `half_char=False`
font.text(display, "HELLO", 32, 16, show=True, clear=True, half_char=False)
time.sleep(1)

# 显示的文字如果很长，会超出屏幕边界，例如：
poem = "他日若遂凌云志，敢笑黄巢不丈夫!"
font.text(display, poem, 0, 8, show=True, clear=True)
time.sleep(1)

# 此时，需要指定参数 `auto_wrap=True` 来自动换行
font.text(display, poem, 0, 8, show=True, clear=True, auto_wrap=True)
time.sleep(1)

# 自动换行的行间距太小了？
# 添加 `line_spacing: int` 参数来调整行间距, 此处指定 8 个像素
font.text(display, poem, 0, 8, show=True, clear=True, auto_wrap=True, line_spacing=8)
time.sleep(1)

# 调整字体大小，可以指定 `font_size: int` 参数
# 注意：这会严重增加运行时间
font.text(display, "T:15℃", 24, 8, font_size=32, show=True, clear=True)
time.sleep(1)

# 当你使用墨水屏时，颜色可能会出现反转。或者你主动想要颜色反转
# 可以指定参数 `reverse=Ture`
font.text(display, "T:15℃", 24, 8, font_size=32, show=True, clear=True, reverse=True)
time.sleep(1)
'''

# 字模生成地址 https://www.zhetao.com/fontarray.html
# 16x16点阵字模（"福"字）
fu = bytearray([
    0x40, 0x00, 
    0x23, 0xfe, 
    0x20, 0x00, 
    0xf9, 0xfc, 
    0x11, 0x04, 
    0x11, 0x04, 
    0x21, 0xfc, 
    0x30, 0x00, 
    0x6b, 0xfe, 
    0xaa, 0x22, 
    0x22, 0x22, 
    0x23, 0xfe, 
    0x22, 0x22, 
    0x22, 0x22, 
    0x23, 0xfe, 
    0x22, 0x02
])

# ===== 图片数据示例 =====
folder_open = bytearray([
    0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 
    0x0f, 0xfc, 0x00, 0x00, 
    0x1f, 0xfe, 0x00, 0x00, 
    0x1f, 0xff, 0x00, 0x00, 
    0x1f, 0xff, 0xff, 0xe0, 
    0x1f, 0xff, 0xff, 0xf0, 
    0x1f, 0xff, 0xff, 0xf0, 
    0x18, 0x00, 0x00, 0x00, 
    0x18, 0x00, 0x00, 0x00, 
    0x18, 0xff, 0xff, 0xfe, 
    0x18, 0xff, 0xff, 0xfe, 
    0x18, 0xff, 0xff, 0xfc, 
    0x19, 0xff, 0xff, 0xfc, 
    0x19, 0xff, 0xff, 0xfc, 
    0x19, 0xff, 0xff, 0xfc, 
    0x19, 0xff, 0xff, 0xf8, 
    0x1b, 0xff, 0xff, 0xf8, 
    0x1b, 0xff, 0xff, 0xf8, 
    0x1f, 0xff, 0xff, 0xf0, 
    0x1f, 0xff, 0xff, 0xf0, 
    0x1f, 0xff, 0xff, 0xf0, 
    0x1f, 0xff, 0xff, 0xe0, 
    0x0f, 0xff, 0xff, 0xc0, 
    0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00, 
    0x00, 0x00, 0x00, 0x00
])

display.show_chinese(30, 23, fu)
display.show_image(50, 16, folder_open, 32, 32)
display.show_chinese(85, 23, fu)
font.text(display, "中国智造惠及全球", 0, 0)
display.text("ESP32-C3:", 10, 48)
#display.fill(0)
display.show()

n=0
while True:
    n+=1
    # 清除位置x,y,清除大小w,h，颜色0，1
    display.fill_rect(82, 47, 46, 9,1)
    display.text(str(n), 82, 48,0)
    display.show()

      