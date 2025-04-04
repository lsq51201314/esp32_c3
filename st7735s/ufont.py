import time
import struct
import framebuf

class BMFont:
    def text(self, display, string: str, x: int, y: int,
             color: int = 0xFFFF, bg_color: int = 0, font_size: int = None,
             half_char: bool = True, auto_wrap: bool = False, show: bool = True, clear: bool = False,
             alpha_color: bool = 0, reverse: bool = False, color_type: int = 1, line_spacing: int = 0, **kwargs):
        """
        Args:
            display: 显示对象
            string: 显示文字
            x: 字符串左上角 x 轴
            y: 字符串左上角 y 轴
            color: 字体颜色(RGB565)
            bg_color: 字体背景颜色(RGB565)
            font_size: 字号大小
            half_char: 半宽显示 ASCII 字符
            auto_wrap: 自动换行
            show: 实时显示
            clear: 清除之前显示内容
            alpha_color: 透明色(RGB565) 当颜色与 alpha_color 相同时则透明
            reverse: 逆置(MONO)
            color_type: 色彩模式 0:MONO 1:RGB565
            line_spacing: 行间距
            **kwargs:
        """
        font_size = font_size or self.font_size
        initial_x = x

        if color_type == -1 and (display.width * display.height) > len(display.buffer):
            color_type = 0
        elif color_type == -1 or color_type == 1:
            palette = [[(bg_color >> 8) & 0xFF, bg_color & 0xFF], [(color >> 8) & 0xFF, color & 0xFF]]
            color_type = 1
            
        if color_type == 0 and color == 0 != bg_color or color_type == 0 and reverse:
            reverse = True
            alpha_color = -1
        else:
            reverse = False

        try:
            display.clear() if clear else 0
        except AttributeError:
            print("请自行调用 display.fill() 清屏")

        for char in range(len(string)):
            if auto_wrap and ((x + font_size // 2 > display.width and ord(string[char]) < 128 and half_char) or
                              (x + font_size > display.width and (not half_char or ord(string[char]) > 128))):
                y += font_size + line_spacing
                x = initial_x

            if string[char] == '\n':
                y += font_size + line_spacing
                x = initial_x
                continue
            elif string[char] == '\t':
                x = ((x // font_size) + 1) * font_size + initial_x % font_size
                continue
            elif ord(string[char]) < 16:
                continue

            if x > display.width or y > display.height:
                continue

            byte_data = list(self.get_bitmap(string[char]))
            if color_type == 0:
                byte_data = self._reverse_byte_data(byte_data) if reverse else byte_data
                if font_size == self.font_size:
                    display.blit(framebuf.FrameBuffer(bytearray(byte_data), font_size, font_size, framebuf.MONO_HLSB),
                                 x, y,
                                 alpha_color)
                else:
                    display.blit(
                        framebuf.FrameBuffer(self._HLSB_font_size(byte_data, font_size, self.font_size), font_size,
                                             font_size, framebuf.MONO_HLSB), x, y, alpha_color)
            elif color_type == 1 and font_size == self.font_size:
                display.blit(framebuf.FrameBuffer(self._flatten_byte_data(byte_data, palette), font_size, font_size,
                                                  framebuf.RGB565), x, y, alpha_color)
            elif color_type == 1 and font_size != self.font_size:
                display.blit(framebuf.FrameBuffer(self._RGB565_font_size(byte_data, font_size, palette, self.font_size),
                                                  font_size, font_size, framebuf.RGB565), x, y, alpha_color)
                
            if ord(string[char]) < 128 and half_char:
                x += font_size // 2
            else:
                x += font_size

        display.show() if show else 0

    def _get_index(self, word: str) -> int:
        """
        获取索引
        Args:
            word: 字符

        Returns:
        ESP32-C3: Function _get_index Time =  2.670ms
        """
        word_code = ord(word)
        start = 0x10
        end = self.start_bitmap

        while start <= end:
            mid = ((start + end) // 4) * 2
            self.font.seek(mid, 0)
            target_code = struct.unpack(">H", self.font.read(2))[0]
            if word_code == target_code:
                return (mid - 16) >> 1
            elif word_code < target_code:
                end = mid - 2
            else:
                start = mid + 2
        return -1

    def _HLSB_font_size(self, byte_data: bytearray, new_size: int, old_size: int) -> bytearray:
        old_size = old_size
        _temp = bytearray(new_size * ((new_size >> 3) + 1))
        _new_index = -1
        for _col in range(new_size):
            for _row in range(new_size):
                if (_row % 8) == 0:
                    _new_index += 1
                _old_index = int(_col / (new_size / old_size)) * old_size + int(_row / (new_size / old_size))
                _temp[_new_index] = _temp[_new_index] | (
                        (byte_data[_old_index >> 3] >> (7 - _old_index % 8) & 1) << (7 - _row % 8))
        return _temp

    def _RGB565_font_size(self, byte_data: bytearray, new_size: int, palette: list, old_size: int) -> bytearray:
        old_size = old_size
        _temp = []
        _new_index = -1
        for _col in range(new_size):
            for _row in range(new_size):
                if (_row % 8) == 0:
                    _new_index += 1
                _old_index = int(_col / (new_size / old_size)) * old_size + int(_row / (new_size / old_size))
                _temp.extend(palette[byte_data[_old_index // 8] >> (7 - _old_index % 8) & 1])
        return bytearray(_temp)

    def _flatten_byte_data(self, _byte_data: bytearray, palette: list) -> bytearray:
        """
        渲染彩色像素
        Args:
            _byte_data:
            palette:

        Returns:

        """
        _temp = []
        for _byte in _byte_data:
            for _b in range(7, -1, -1):
                _temp.extend(palette[(_byte >> _b) & 0x01])
        return bytearray(_temp)

    def _reverse_byte_data(self, _byte_data: bytearray) -> bytearray:
        for _pixel in range(len(_byte_data)):
            _byte_data[_pixel] = ~_byte_data[_pixel] & 0xff
        return _byte_data

    def get_bitmap(self, word: str) -> bytes:
        """获取点阵图

        Args:
            word: 字符

        Returns:
            bytes 字符点阵
        """
        index = self._get_index(word)
        if index == -1:
            return b'\xff\xff\xff\xff\xff\xff\xff\xff\xf0\x0f\xcf\xf3\xcf\xf3\xff\xf3\xff\xcf\xff?\xff?\xff\xff\xff' \
                   b'?\xff?\xff\xff\xff\xff'

        self.font.seek(self.start_bitmap + index * self.bitmap_size, 0)
        return self.font.read(self.bitmap_size)

    def __init__(self, font_file):
        """
        Args:
            font_file: 字体文件路径
        """
        self.font_file = font_file
        self.font = open(font_file, "rb")
        self.bmf_info = self.font.read(16)
        if self.bmf_info[0:2] != b"BM":
            raise TypeError("字体文件格式不正确: " + font_file)
        self.version = self.bmf_info[2]
        if self.version != 3:
            raise TypeError("字体文件版本不正确: " + str(self.version))
        self.map_mode = self.bmf_info[3]
        self.start_bitmap = struct.unpack(">I", b'\x00' + self.bmf_info[4:7])[0]
        self.font_size = self.bmf_info[7]
        self.bitmap_size = self.bmf_info[8]
