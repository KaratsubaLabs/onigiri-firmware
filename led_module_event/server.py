
'''
API

turn light on
{ state: 'on' }

turn light off
{ state: 'off' }

'''

import socket
import network
import json

TIMEOUT = 20
MAX_BODY_SIZE = 4096

URL = '167.99.178.60'
PORT = 80
HOST = 'home.karatsubalabs.com'

def server():

    sta_if = network.WLAN(network.STA_IF)
    print(sta_if.ifconfig())

    addr = socket.getaddrinfo(URL, PORT)[0][-1]

    s = socket.socket()
    s.connect(addr)

    payload = 'GET /v1beta/device/event_test HTTP/1.1\nHost: ' + HOST +'\n\n'
    print(payload)
    r = s.send(payload)
    while True:

        req = str(s.recv(4096))
        print(req)
        try:
            req = req[2:-1]
            req = req.split('\\r\\n', 2)
            payload = req[1][5:-2]
            print(parsed + ' ' + json.loads(payload))
        except:
            pass 

    s.close()

    
