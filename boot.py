import machine
import network


def init():
    machine.freq(240000000)


def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect('roolin', 'niloor666')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


# if __name__ == '__main__':
    init()
#     do_connect()
