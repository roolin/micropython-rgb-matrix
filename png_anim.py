from matrix import Matrix
import time, machine


class PngAnim:
    def __init__(self, png, lines):
        self.png = png
        self.lines = lines
        self.frames = []
        self.matrixes = []
        self.cut_frames()
        self.prep_matrix()

    def cut_frames(self):
        f = []
        count = self.lines
        for l in self.png:
            f.append(l)
            if len(f) == self.lines:
                self.frames.append(f)
                f = []

    def prep_matrix(self):
        self.matrixes = []
        for f in self.frames:
            m = Matrix(len(self.frames[0]), self.lines, True)
            m.bitmap(f)
            self.matrixes.append(m)

    def show(self, delay, pin):
        for m in self.matrixes:
            m.light(pin)
            time.sleep_ms(delay)


import round
a = Animation(round.round_data(), 16)


def test(delay):
    pin = machine.Pin(25)
    pin.init(pin.OUT)
    while True:
        a.show(delay, pin)

