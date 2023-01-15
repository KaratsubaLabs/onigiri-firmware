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
    pin_5 = Pin(5, Pin.OUT)

    sta_if = network.WLAN(network.STA_IF)  # station interface
    ap_if = network.WLAN(network.AP_IF)  # access point interface

    sta_if.active(True)
    ap_if.active(False)

    time.sleep(3)
    count = 0
    while (not sta_if.isconnected()):
        if count > NETWORK_RETRIES:
            break
        for j in range(5):
            pin_5.on()
            time.sleep(0.1)
            pin_5.off()
            time.sleep(0.1)

        try:
            sta_if.connect(config.SSID, config.PSK)
        except:
            print("internal wifi error")

        time.sleep(1)
        if sta_if.isconnected():
            break

    if sta_if.isconnected():
        pin_5.on()
        return True
    else:
        pin_5.off()
        return False


def ping_server():

    import urequests

    sta_if = network.WLAN(network.STA_IF)
    # TODO assert connected to internet
    ip_addr = sta_if.ifconfig()[0]

    body = {
        'name': config.DEVICE_NAME,
        'ip_address': ip_addr,
        'api_type': config.API_TYPE,
    }
    res = urequests.post(config.SERVER_ADDR + '/v1beta/device', json=body)
    if res.status_code != 200:
        print('error pinging server')


def mac_address():
    import ubinascii
    sta_if = network.WLAN(network.STA_IF)
    return ubinascii.hexlify(sta_if.config('mac'), ':').decode().upper()


if network_connect():

    try:
        ping_server()
    except:
        print('failed to ping server')

    import server
    server.server()
