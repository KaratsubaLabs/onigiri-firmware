## translated from https://github.com/brantje/rpi-16x2-lcd/blob/master/lcd.py

## GPIO Layout
# GPIO4 - RS
# GPIO2 - E

# GPIO14 - D4
# GPIO12 - D5
# GPIO13 - D6
# GPIO15 - D7

from machine import Pin
import time

_DISPLAY_WIDTH = 16

E_PULSE = 0.0005
E_DELAY = 0.0005

CHR_MODE = True
CMD_MODE = False

LINE_ONE = 0x80
LINE_TWO = 0xC0

pin_rs = Pin(4, Pin.OUT)
pin_e = Pin(2, Pin.OUT)
pin_d4 = Pin(14, Pin.OUT)
pin_d5 = Pin(12, Pin.OUT)
pin_d6 = Pin(13, Pin.OUT)
pin_d7 = Pin(15, Pin.OUT)


# mode indicates mode of operation
#   true - character mode
#   false - command mode
def write_byte(data, mode):
    if mode:
        pin_rs.on()
    else:
        pin_rs.off()

    # high bits
    pin_d4.value(data & 0x10 == 0x10)
    pin_d5.value(data & 0x20 == 0x20)
    pin_d6.value(data & 0x40 == 0x40)
    pin_d7.value(data & 0x80 == 0x80)

    pulse_e()

    # low bits
    pin_d4.value(data & 0x01 == 0x01)
    pin_d5.value(data & 0x02 == 0x02)
    pin_d6.value(data & 0x04 == 0x04)
    pin_d7.value(data & 0x08 == 0x08)

    pulse_e()


def pulse_e():
    pin_e.off()
    time.sleep(E_DELAY)
    pin_e.on()
    time.sleep(E_PULSE)
    pin_e.off()
    time.sleep(E_DELAY)


def init():
    write_byte(0x33, CMD_MODE)  # init sequence
    write_byte(0x32, CMD_MODE)  # init sequence
    write_byte(0x06, CMD_MODE)
    write_byte(0x0D, CMD_MODE)
    write_byte(0x28, CMD_MODE)
    write_byte(0x01, CMD_MODE)
    time.sleep(E_DELAY)


def clear_screen():
    write_byte(0x06, CMD_MODE)
    write_byte(0x01, CMD_MODE)
    time.sleep(0.5)


def set_line(line):
    write_byte(line, CMD_MODE)


def display(msg, speed=0.05):
    fmt = '{msg: <{fill}}'.format(msg=msg[0:_DISPLAY_WIDTH],
                                  fill=_DISPLAY_WIDTH)
    for c in fmt:
        write_byte(ord(c), CHR_MODE)
        time.sleep(speed)


def test():
    init()
    set_line(LINE_TWO)
    display('hello world!')
    time.sleep(1)
