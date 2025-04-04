from micropython import const
from machine import Pin
from time import sleep_us, sleep_ms
 
TM1637_CMD1 = const(64)
TM1637_CMD2 = const(192)
TM1637_CMD3 = const(128)
TM1637_DSP_ON = const(8)
TM1637_DELAY = const(10)
TM1637_MSB = const(128)

_SEGMENTS = bytearray(b'\x3F\x06\x5B\x4F\x66\x6D\x7D\x07\x7F\x6F\x77\x7C\x39\x5E\x79\x71\x3D\x76\x06\x1E\x76\x38\x55\x54\x3F\x73\x67\x50\x6D\x78\x3E\x1C\x2A\x76\x6E\x5B\x00\x40\x63')
 
class TM1637(object):
    def __init__(self, clk, dio, brightness=7):
        self.clk = clk
        self.dio = dio
 
        if not 0 <= brightness <= 7:
            raise ValueError("Brightness out of range")
        self._brightness = brightness
 
        self.clk.init(Pin.OUT, value=0)
        self.dio.init(Pin.OUT, value=0)
        sleep_us(TM1637_DELAY)
 
        self._write_data_cmd()
        self._write_dsp_ctrl()
 
    def _start(self):
        self.dio(0)
        sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)
 
    def _stop(self):
        self.dio(0)
        sleep_us(TM1637_DELAY)
        self.clk(1)
        sleep_us(TM1637_DELAY)
        self.dio(1)
 
    def _write_data_cmd(self):
        self._start()
        self._write_byte(TM1637_CMD1)
        self._stop()
 
    def _write_dsp_ctrl(self):
        self._start()
        self._write_byte(TM1637_CMD3 | TM1637_DSP_ON | self._brightness)
        self._stop()
 
    def _write_byte(self, b):
        for i in range(8):
            self.dio((b >> i) & 1)
            sleep_us(TM1637_DELAY)
            self.clk(1)
            sleep_us(TM1637_DELAY)
            self.clk(0)
            sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)
        self.clk(1)
        sleep_us(TM1637_DELAY)
        self.clk(0)
        sleep_us(TM1637_DELAY)
 
    def brightness(self, val=None):
        if val is None:
            return self._brightness
        if not 0 <= val <= 7:
            raise ValueError("Brightness out of range")
 
        self._brightness = val
        self._write_data_cmd()
        self._write_dsp_ctrl()
 
    def write(self, segments, pos=0):
        if not 0 <= pos <= 5:
            raise ValueError("Position out of range")
        self._write_data_cmd()
        self._start()
 
        self._write_byte(TM1637_CMD2 | pos)
        for seg in segments:
            self._write_byte(seg)
        self._stop()
        self._write_dsp_ctrl()
 
    def encode_digit(self, digit):
        return _SEGMENTS[digit & 0x0f]
 
    def encode_string(self, string):
        segments = bytearray(len(string))
        for i in range(len(string)):
            segments[i] = self.encode_char(string[i])
        return segments
 
    def encode_char(self, char):
        o = ord(char)
        if o == 32:
            return _SEGMENTS[36] 
        if o == 42:
            return _SEGMENTS[38] 
        if o == 45:
            return _SEGMENTS[37] 
        if o >= 65 and o <= 90:
            return _SEGMENTS[o-55] 
        if o >= 97 and o <= 122:
            return _SEGMENTS[o-87] 
        if o >= 48 and o <= 57:
            return _SEGMENTS[o-48] 
        raise ValueError("Character out of range: {:d} '{:s}'".format(o, chr(o)))
 
    def hex(self, val):
        string = '{:04x}'.format(val & 0xffff)
        self.write(self.encode_string(string))
 
    def number(self, num):
        num = max(-999, min(num, 9999))
        string = '{0: >4d}'.format(num)
        self.write(self.encode_string(string))
 
    def numbers(self, num1, num2, colon=True):
        num1 = max(-9, min(num1, 99))
        num2 = max(-9, min(num2, 99))
        segments = self.encode_string('{0:0>2d}{1:0>2d}'.format(num1, num2))
        if colon:
            segments[1] |= 0x80
        self.write(segments)
 
    def temperature(self, num):
        if num < -9:
            self.show('lo')
        elif num > 99:
            self.show('hi')
        else:
            string = '{0: >2d}'.format(num)
            self.write(self.encode_string(string))
        self.write([_SEGMENTS[38], _SEGMENTS[12]], 2)
 
    def show(self, string, colon=False):
        segments = self.encode_string(string)
        if len(segments) > 1 and colon:
            segments[1] |= 128
        self.write(segments[:4])
 
    def scroll(self, string, delay=250):
        segments = string if isinstance(string, list) else self.encode_string(string)
        data = [0] * 8
        data[4:0] = list(segments)
        for i in range(len(segments) + 5):
            self.write(data[0+i:4+i])
            sleep_ms(delay)
 
 
class TM1637Decimal(TM1637):
    def encode_string(self, string):
        segments = bytearray(len(string.replace('.','')))
        j = 0
        for i in range(len(string)):
            if string[i] == '.' and j > 0:
                segments[j-1] |= TM1637_MSB
                continue
            segments[j] = self.encode_char(string[i])
            j += 1
        return segments