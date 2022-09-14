
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

E_PULSE = 0.0005
E_DELAY = 0.0005

CHR_MODE = True
CMD_MODE = False

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

    # print("=-=-=-=")
    # print(data & 0x10 == 0x10)
    # print(data & 0x20 == 0x20)
    # print(data & 0x40 == 0x40)
    # print(data & 0x80 == 0x80)
    # pin_d4.value(data & 0x10 == 0x10)
    # pin_d5.value(data & 0x20 == 0x20)
    # pin_d6.value(data & 0x40 == 0x40)
    # pin_d7.value(data & 0x80 == 0x80)

    # high bits
    pin_d4.off()
    pin_d5.off()
    pin_d6.off()
    pin_d7.off()
    if data & 0x10 == 0x10:
        pin_d4.on()
    if data & 0x20 == 0x20:
        pin_d5.on()
    if data & 0x40 == 0x40:
        pin_d6.on()
    if data & 0x80 == 0x80:
        pin_d7.on()

    pulse_e()

    # low bits
    pin_d4.off()
    pin_d5.off()
    pin_d6.off()
    pin_d7.off()
    if data & 0x01 == 0x01:
        pin_d4.on()
    if data & 0x02 == 0x02:
        pin_d5.on()
    if data & 0x04 == 0x04:
        pin_d6.on()
    if data & 0x08 == 0x08:
        pin_d7.on()

    pulse_e()

def pulse_e():
    pin_e.off()
    time.sleep(E_DELAY)
    pin_e.on()
    time.sleep(E_PULSE)
    pin_e.off()
    time.sleep(E_DELAY)


def init():
    write_byte(0x33, CMD_MODE)
    write_byte(0x32, CMD_MODE)
    write_byte(0x06, CMD_MODE)
    write_byte(0x0D, CMD_MODE)
    write_byte(0x28, CMD_MODE)
    write_byte(0x01, CMD_MODE)
    time.sleep(E_DELAY)
     
def clear_screen():
    write_byte(0x06, CMD_MODE)
    write_byte(0x01, CMD_MODE)
    time.sleep(0.5)

def set_line1():
    write_byte(0x80, CMD_MODE)

def set_line2():
    write_byte(0xC0, CMD_MODE)

def test():
    init()
    clear_screen()
    set_line2()
    for i in range(16):
        write_byte(ord('A'), CHR_MODE)
        time.sleep(0.2)

    time.sleep(1)

def all_on():
    pin_d4.on()
    pin_d5.on()
    pin_d6.on()
    pin_d7.on()


