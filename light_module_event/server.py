
'''
API

turn light on
{ updates: [{ room: 'room name', state: 'on' }] }

'''

import time
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

room_lights = {
    'master bedroom south': Pin(27, Pin.OUT),
    'bathroom': Pin(19, Pin.OUT),
    'kids bedroom': Pin(22, Pin.OUT),
    'living room': Pin(18, Pin.OUT),
    'kitchen': Pin(23, Pin.OUT),
    'master bedroom north': Pin(32, Pin.OUT)
}

def server():

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

        try:
            for update in parsed['updates']:
                room = update['room']
                state = update['state']

                if state == 'on':
                    room_lights[room].on()
                elif state == 'off':
                    room_lights[room].off()
                else:
                    print('invalid state: ' + state)
        except:
            print('issue controlling lights')


    s.close()

    
