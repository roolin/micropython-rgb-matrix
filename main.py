import time, ripples, button, matrix
from machine import Pin


def run():
    but = button.Button(32)
    r = ripples.RipplesAnim(25, 16)

    start = time.ticks_ms()
    button_val = but.check()

    stop = False
    while not stop:
        new_val = but.check()
        if button_val != new_val and new_val == 0:
            stop = True
        button_val = new_val
        r.next_step()

    m = matrix.Matrix(16, 16)
    pin = Pin(25)
    pin.init(pin.OUT)
    m.clear()
    m.light(pin)

    stop = time.ticks_ms()
    print(str(stop - start))
    print(r.light)


# if __name__ == '__main__':
#     run()
