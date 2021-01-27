import time
import machine
from esp import neopixel_write


class Matrix:
    def __init__(self, x_size, y_size, sum_mode=False):
        self.leds = bytearray(x_size * y_size * 3)
        self.x_size = x_size
        self.y_size = y_size
        self.sum_mode = sum_mode

    @micropython.viper
    def set_pixel(self, point, color):
        r, g, b = color
        x, y = point
        led = int(self.led_by_xy(x, y))
        index = led * 3
        leds = self.leds
        if not self.sum_mode or (int(leds[index]) == 0 and int(leds[index+1]) == 0 and int(leds[index+2]) == 0):
            leds[index] = r
            leds[index+1] = g
            leds[index+2] = b
        else:
            leds[index] = int(int(leds[index]) + int(r)) >> 1
            leds[index + 1] = int(int(leds[index + 1]) + int(g)) >> 1
            leds[index + 2] = int(int(leds[index + 2]) + int(b)) >> 1

    @micropython.viper
    def set_pixels(self, pixels, color):
        f_sp = self.set_pixel
        for p in pixels:
            f_sp(p, color)

    @micropython.native
    def light(self, pin):
        neopixel_write(pin, self.leds, True)

    @micropython.viper
    def led_by_xy(self, x: int, y: int) -> int:
        xs = int(self.x_size)
        ys = int(self.y_size)

        o_n = xs * (ys - y - 1)

        if y & 1 == 1:
            o_n += x
        else:
            o_n += (xs - x - 1)
        return o_n

    @micropython.native
    def one_color(self, r, g, b):
        for i in range(self.x_size * self.y_size):
            self.leds[i * 3] = r
            self.leds[i * 3 + 1] = g
            self.leds[i * 3 + 2] = b

    @micropython.native
    def clear(self):
        self.leds = bytearray(self.x_size * self.y_size * 3)

    @micropython.native
    def bitmap(self, picture):
        row = 0
        for a in picture:
            col = 0
            rgb = []
            for pc in a:
                rgb.append(pc)
                if len(rgb) == 4:
                    self.set_pixel((rgb[0] >> 3, rgb[1] >> 3, rgb[2] >> 3), (col, row))
                    rgb = []
                    col += 1
            row += 1


@micropython.native
def test2(mode):
    pixels = []
    for i in range(16):
        pixels.append((0, i))
        pixels.append((2, i))
        pixels.append((4, i))
        pixels.append((6, i))
        pixels.append((8, i))
        pixels.append((10, i))
        pixels.append((12, i))
        pixels.append((14, i))

    pin = machine.Pin(25, machine.Pin.OUT)
    m = Matrix(16, 16, mode)

    start = time.ticks_us()
    m.set_pixels(pixels, (4, 0, 2))
    m.set_pixels(pixels, (4, 0, 2))
    m.set_pixels(pixels, (4, 0, 2))
    m.set_pixels(pixels, (4, 0, 2))
    stop = time.ticks_us()
    print(stop - start)
    m.light(pin)

    start = time.ticks_us()
    m.set_pixels_2(pixels, (4, 0, 2))
    m.set_pixels_2(pixels, (4, 0, 2))
    m.set_pixels_2(pixels, (4, 0, 2))
    m.set_pixels_2(pixels, (4, 0, 2))
    stop = time.ticks_us()
    print(stop - start)
    m.light(pin)