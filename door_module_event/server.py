import servo
import time
import socket
import network
import config
import ujson

TIMEOUT = 20
MAX_BODY_SIZE = 4096

URL = '167.99.178.60'
PORT = 80
HOST = 'home.karatsubalabs.com'

DOOR_OPEN_SERVO_ANGLE = 90
DOOR_CLOSED_SERVO_ANGLE = 0

servo.init(DOOR_CLOSED_SERVO_ANGLE)


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

        if parsed['state'] == 'open':
            servo.set_angle(DOOR_OPEN_SERVO_ANGLE)
        elif parsed['state'] == 'closed':
            servo.set_angle(DOOR_CLOSED_SERVO_ANGLE)
        else:
            print('invalid state: ' + parsed['state'])

    s.close()

    
