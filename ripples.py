from random import randint
import time


class Squere:
    def __init__(self, center, size, max_size):
        self.center = center
        self.size = size
        self.max_size = max_size

    @micropython.native
    def get_shape(self):
        size = self.size
        max_size = self.max_size
        cx, cy = self.center
        modifier = int(size / 2)
        x, y = cx - modifier, cy - modifier
        coor = []
        nx, ny = 0, 0
        for i in range(size):
            x_s = x + i
            if 0 <= x_s < max_size:
                if 0 <= y < max_size:
                    coor.append((x_s, y))
                if 0 <= y + size - 1 < max_size:
                    coor.append((x_s, y + size - 1))
        for i in range(size - 2):
            y_s = y + 1 + i
            if 0 <= y_s < max_size:
                if 0 <= x < max_size:
                    coor.append((x, y_s))
                if 0 <= x + size - 1 < max_size:
                    coor.append((x + size - 1, y_s))

        return coor

    @micropython.native
    def move(self, x, y):
        xm, ym = self.center
        self.center = x + xm, y + ym

    @micropython.native
    def resize(self, change: int):
        self.size = self.size + change


class Ripples:
    def __init__(self, center, color, max_size):
        self.center = center
        self.color = color
        self.max_size = max_size
        self.squeres = [Squere(center, 1, max_size)]

    @micropython.native
    def next_step(self):
        sq = []
        shift = 0
        new_color = None
        for s in self.squeres:
            r, g, b = self.color
            new_color = (r >> shift, g >> shift, b >> shift)
            shape = s.get_shape()
            if shape and new_color != (0, 0, 0):
                sq.append((shape, new_color))
            s.resize(2)
            shift += 1

        if new_color != (0, 0, 0):
            self.squeres.append(Squere(self.center, 1, self.max_size))

        return sq

    def reset(self, center, color):
        self.center = center
        self.color = color
        self.squeres = [Squere(center, 1, self.max_size)]


class RipplesAnim:
    def __init__(self, gpio, max_size):
        from machine import Pin
        from matrix import Matrix
        import time
        self.max_size = max_size
        self.matrix = Matrix(max_size, max_size, True)
        r1 = Ripples((4, 4), (127, 0, 0), max_size)
        r2 = Ripples((12, 12), (0, 127, 0), max_size)
        r3 = Ripples((12, 4), (0, 0, 127), max_size)
        r4 = Ripples((4, 12), (0, 127, 127), max_size)
        self.rips = [r1, r2, r3, r4]
        self.pin = Pin(gpio, Pin.OUT)
        # self.pin.init(self.pin.OUT)
        self.curr_time = time.ticks_ms()

    def next_step(self):
        for r in self.rips:
            ns = r.next_step()
            if ns:
                for pix, col in ns:
                    self.matrix.set_pixels(pix, col)
            else:
                r.reset((randint(0, self.max_size), randint(0, self.max_size)), (randint(0, 255), randint(0, 255), randint(0, 255)))
        self.curr_time = time.ticks_ms()
        self.matrix.light(self.pin)


def test2():
    import time
    r = RipplesAnim(25, 16)

    start = time.ticks_ms()
    ns = r.next_step
    for i in range(20):
        ns()
    stop = time.ticks_ms()
    print(str(stop - start))
