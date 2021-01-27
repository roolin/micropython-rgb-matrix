from machine import Pin
import time


class Button:
    def __init__(self, gpio, debounce_ms=10):
        self.pin = Pin(gpio, Pin.IN, Pin.PULL_UP)
        self.value = 1
        self.last_val = 1
        self.last_change = time.ticks_us()
        self.debounce_ms = debounce_ms

    def check(self):
        val = self.pin.value()
        now = time.ticks_us()
        if val != self.last_val:
            self.last_val = val
            self.last_change = now
        elif now - self.last_change > self.debounce_ms:
            self.value = self.last_val
        return self.value
