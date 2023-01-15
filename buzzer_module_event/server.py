

'''
API

turn alarm on
{ state: 'on' }

'''

import socket
import network
import ujson
import config
import time
from machine import Pin, PWM

TIMEOUT = 20
MAX_BODY_SIZE = 4096

URL = '167.99.178.60'
PORT = 80
HOST = 'home.karatsubalabs.com'

def server():
    
    pin_18 = Pin(18, Pin.OUT)

    sta_if = network.WLAN(network.STA_IF)
    print(sta_if.ifconfig())

    addr = socket.getaddrinfo(URL, PORT)[0][-1]

    s = socket.socket()
    s.connect(addr)

    payload = 'GET /v1beta/event/device/' + config.DEVICE_NAME + ' HTTP/1.1\nHost: ' + HOST +'\n\n'
    print(payload)
    r = s.send(payload)

    pin_18.off()

    while True:

        req = str(s.recv(4096))[2:-1]
        if len(req) == 0:
            continue

        req = req.lstrip('data:')
        req = req.rstrip('\\n')
        print(req)

        try:
            parsed = ujson.loads(req)
            print('parsed' + str(parsed))
        except Exception as e:
            print('json exception '+str(e))
            continue

        if parsed['state'] == 'on':
            for i in range(5):
                time.sleep(1)
                pin_18.on()
                time.sleep(1)
                pin_18.off()
        else:
            print('invalid state: ' + parsed['state'])

    s.close()
    
