from random import randint
from time import ticks_ms


class Wave:
    def __init__(self, color, size, direction):
        self.color = color
        self.step = 1
        self.size = size
        self.direction = direction
        self.colors = []
        self.prepare_colors()

    def prepare_colors(self):
        c = self.color
        self.colors = []
        while c != (0, 0, 0):
            self.colors.append(c)
            c = (c[0] >> 1, c[1] >> 1, c[2] >> 1)
        self.colors.reverse()
        self.colors.extend(reversed(self.colors[0:len(self.colors) - 1]))

    @micropython.native
    def next_step(self):
        start = 0
        step = self.step
        if step > len(self.colors):
            start = step - len(self.colors)
        stop = step
        modif = 0
        if step > self.size * 2 - 1:
            stop = self.size * 2 - 1
            modif = step - (self.size * 2 - 1)
        points = []
        f_get_line = self.get_line
        colors = self.colors
        for idx, i in enumerate(reversed(range(start, stop))):
            points.append((f_get_line(i+1), colors[idx+modif]))

        self.step += 1
        return points

    @micropython.viper
    def get_line(self, ordinal: int):
        points = []
        start = 0
        size = int(self.size)
        if ordinal > size:
            start = ordinal - size
        direction = int(self.direction)
        shift = size - 1
        for i in range(start, ordinal - start):
            if direction == 0:
                points.append((i, (ordinal - i - 1)))
            elif direction == 1:
                points.append((shift - i, (ordinal - i - 1)))
            elif direction == 2:
                points.append((shift - i, shift - (ordinal - i - 1)))
            elif direction == 3:
                points.append((i, shift - (ordinal - i - 1)))
        return points

    def reset(self, color):
        self.direction += 1
        if self.direction > 3:
            self.direction = 0
        self.step = 1
        self.color = color
        self.prepare_colors()


class ContinuousWave:
    def __init__(self, size, direction):
        self.size = size
        self.direction = direction
        self.waves = []

    @micropython.native
    def step(self):
        if not self.waves:
            self.add_wave()
        rem = False
        pixels = []
        for w in self.waves:
            ns = w.next_step()
            if not ns:
                rem = True
            if w.step - 1 == len(w.colors):
                self.add_wave()
            pixels.append(ns)
        if rem:
            del self.waves[0]
        return pixels

    def add_wave(self):
        return self.waves.append(Wave((randint(0, 255), randint(0, 255), randint(0, 255)), self.size, self.direction))


@micropython.native
def test():
    from matrix import Matrix
    from machine import Pin

    matrix = Matrix(16, 16, True)
    pin = Pin(25, Pin.OUT)

    cw1 = ContinuousWave(16, 0)
    cw2 = ContinuousWave(16, 1)
    cw3 = ContinuousWave(16, 2)
    cw4 = ContinuousWave(16, 3)

    waves = [cw1, cw3]

    start = ticks_ms()
    while True:
        for w in waves:
            px = w.step()
            for l in px:
                for line, color in l:
                    matrix.set_pixels(line, color)
        matrix.light(pin)
    stop = ticks_ms()
    print(stop - start)
    matrix.clear()
    matrix.light(pin)
