# controller software for L298N motor driver

from machine import Pin
import time

pin_4 = Pin(4, Pin.OUT)
pin_2 = Pin(2, Pin.OUT)


def motor_stop():
    pin_4.off()
    pin_2.off()


def motor_left():
    pin_4.on()
    pin_2.off()


def motor_right():
    pin_4.off()
    pin_2.on()


def test():
    for i in range(10):
        motor_stop()
        time.sleep(1)
        motor_left()
        time.sleep(3)
        motor_stop()
        time.sleep(1)
        motor_right()
        time.sleep(3)


motor_stop()
