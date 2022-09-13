# flash the GPIO5 Led 10 times

from machine import Pin
import time

import network
import config

# amount of times will attempt to connect to internet before failing
NETWORK_RETRIES = 10 

# NETWORK CONNECTION SEQUENCE
#   - blinking when attempting to connect to internet
#   - LED stays on when connection is established
#   - LED says off when failed maximum number of network connection retries
def network_connect():
    pin5 = Pin(5, Pin.OUT)

    sta_if = network.WLAN(network.STA_IF) # station interface
    ap_if = network.WLAN(network.AP_IF)   # access point interface

    sta_if.active(True)
    ap_if.active(False)

    time.sleep(3)
    for i in range(NETWORK_RETRIES):
        for j in range(5):
            pin5.on()
            time.sleep(0.1)
            pin5.off()
            time.sleep(0.1)

        sta_if.connect(config.SSID, config.PSK)
        time.sleep(1)
        if sta_if.isconnected():
            break

    if sta_if.isconnected():
        pin5.on()
        return True
    else:
        pin5.off()
        return False

def mac_address():
    import ubinascii
    return ubinascii.hexlify(sta_if.config('mac'), ':').decode().upper() 

network_connect()
