PORT = 80
TIMEOUT = 20
MAX_BODY_SIZE = 1024

import lcd

lcd.init()

'''
API

write to line 1
{ mode: 'write', text: 'hello world', line: 0 }

clear
{ mode: 'clear' }

'''

import socket
import network
import ujson
import config
from machine import Pin

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

        # TODO hella hacky
        try:
            print(parsed['mode'] + ' ' + parsed['text'] + ' ' + parsed['line'])
        except:
            continue

        if parsed['mode'] == 'write':
            lcd.set_line(line)
        
            line = lcd.LINE_ONE
            if parsed['line'] == '1':
                line = lcd.LINE_ONE
            elif parsed['line'] == '2':
                line = lcd.LINE_TWO

            lcd.set_line(line)
            lcd.display(parsed['text'])
        elif parsed['mode'] == 'clear':
            pass
        else:
            print('invalid mode: ' + parsed['mode'])

    s.close()

    
