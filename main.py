# flash the GPIO5 Led 10 times

from machine import Pin
import time

pin5 = Pin(5, Pin.OUT)
for i in range(0, 10):
    pin5.on()
    time.sleep(1)
    pin5.off()
    time.sleep(1)

