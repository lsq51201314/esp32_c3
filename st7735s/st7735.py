from time import sleep_ms
from ustruct import pack
from machine import SPI,Pin
from micropython import const
import framebuf

NOP     = const(0x00)
SWRESET = const(0x01)
SLPIN   = const(0x10)
SLPOUT  = const(0x11)
PTLON   = const(0x12)
NORON   = const(0x13)
INVOFF  = const(0x20)
INVON   = const(0x21)
DISPOFF = const(0x28)
DISPON  = const(0x29)
CASET   = const(0x2A)
RASET   = const(0x2B)
RAMWR   = const(0x2C)
RGBSET  = const(0x2D)
PTLAR   = const(0x30)
COLMOD  = const(0x3A)
MADCTL  = const(0x36)
FRMCTR1 = const(0xB1)
FRMCTR2 = const(0xB2)
FRMCTR3 = const(0xB3)
INVCTR  = const(0xB4)
PWCTR1  = const(0xC0)
PWCTR2  = const(0xC1)
PWCTR3  = const(0xC2)
PWCTR4  = const(0xC3)
PWCTR5  = const(0xC4)
VMCTR1  = const(0xC5)
GMCTRP1 = const(0xE0)
GMCTRN1 = const(0xE1)

class ST7735(framebuf.FrameBuffer):
    def __init__(self, spi, dc, rst, cs, width=160, height=80, rot=3, bgr=0):
        if dc is None:
            raise RuntimeError('TFT must be initialized with a dc pin number')
        dc.init(dc.OUT, value=0)
        if cs is None:
            raise RuntimeError('TFT must be initialized with a cs pin number')
        cs.init(cs.OUT, value=1)
        if rst is not None:
            rst.init(rst.OUT, value=1)
        else:
            self.rst =None
        self.spi = spi
        self.rot = rot
        self.dc = dc
        self.rst = rst
        self.cs = cs
        self.height = height
        self.width = width
        self.buffer = bytearray(self.height * self.width*2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565, self.width)
        if (self.rot ==0):
            madctl=0x00
        elif (self.rot ==1):
            madctl=0xa0
        elif (self.rot ==2):
            madctl=0xc0
        else :
            madctl=0x60
        if bgr==0:
            madctl|=0x08
        self.madctl = pack('>B', madctl)
        self.reset()

        self._write(SLPOUT)
        sleep_ms(120)
        for command, data in (
            (COLMOD,  b"\x05"),
            (MADCTL,  pack('>B', madctl)),
            ):
            self._write(command, data)
        if self.width==80 or self.height==80:
            self._write(INVON, None)
        else:
            self._write(INVOFF, None)
        buf=bytearray(128)
        for i in range(32):
            buf[i]=i*2
            buf[i+96]=i*2
        for i in range(64):
            buf[i+32]=i
        self._write(RGBSET, buf)
        self.show()
        self._write(DISPON)
        
    def reset(self):
        if self.rst is None:
            self._write(SWRESET)
            sleep_ms(50)
            return
        self.rst.off()
        sleep_ms(50)
        self.rst.on()
        sleep_ms(50)
        
    def _write(self, command, data = None):
        self.cs.off()
        self.dc.off()
        self.spi.write(bytearray([command]))
        self.cs.on()
        if data is not None:
            self.cs.off()
            self.dc.on()
            self.spi.write(data)
            self.cs.on()
            
    def show(self):
        if self.width==80 or self.height==80:
            if self.rot==0 or self.rot==2:
                self._write(CASET,pack(">HH", 26, self.width+26-1))
                self._write(RASET,pack(">HH", 1, self.height+1-1))
            else:
                self._write(CASET,pack(">HH", 1, self.width+1-1))
                self._write(RASET,pack(">HH", 26, self.height+26-1))
        else:
            if self.rot==0 or self.rot==2:
                self._write(CASET,pack(">HH", 0, self.width-1))
                self._write(RASET,pack(">HH", 0, self.height-1))
            else:
                self._write(CASET,pack(">HH", 0, self.width-1))
                self._write(RASET,pack(">HH", 0, self.height-1))
            
        self._write(RAMWR,self.buffer)
        
    def rgb(self,r,g,b):
        return ((r&0xf8)<<8)|((g&0xfc)<<3)|((b&0xf8)>>3)

    def clear(self):
        self.fill(0)

    def show_chinese(self, x, y, font_data, width=16, height=16, fg_color=0xffff, bg_color=0x0000):
        buf_size = width * height * 2
        buffer = bytearray(buf_size)
        fg_bytes = pack('>H', fg_color)
        bg_bytes = pack('>H', bg_color)
        for i in range(len(font_data)):
            byte = font_data[i]
            for bit in range(7, -1, -1): 
                pixel_offset = (i * 8 + (7 - bit)) * 2
                if byte & (1 << bit):
                    buffer[pixel_offset:pixel_offset+2] = fg_bytes
                else:
                    buffer[pixel_offset:pixel_offset+2] = bg_bytes
        fb = framebuf.FrameBuffer(buffer, width, height, framebuf.RGB565)
        self.blit(fb, x, y)

    def show_icon(self, x, y, img_data, width=32, height=32, fg_color=0xffff, bg_color=0x0000):
        buf_size = width * height * 2
        buffer = bytearray(buf_size)
        fg_bytes = pack('>H', fg_color)
        bg_bytes = pack('>H', bg_color)
        for i in range(len(img_data)):
            byte = img_data[i]
            for bit in range(7, -1, -1):  
                pixel_offset = (i * 8 + (7 - bit)) * 2
                if byte & (1 << bit):
                    buffer[pixel_offset:pixel_offset+2] = fg_bytes
                else:
                    buffer[pixel_offset:pixel_offset+2] = bg_bytes
        fb = framebuf.FrameBuffer(buffer, width, height, framebuf.RGB565)
        self.blit(fb, x, y)