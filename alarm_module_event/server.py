

'''
API

enable alarm mode
{ 'state': 'armed' }

disabled alarm mode
{ 'state': 'unarmed' }
'''

import urequests
import socket
import network
import ujson
import config
import sys
from hcsr04 import HCSR04
from machine import Pin, time_pulse_us
import time
import _thread

TIMEOUT = 20
MAX_BODY_SIZE = 4096

URL = '167.99.178.60'
PORT = 80
HOST = 'home.karatsubalabs.com'

THRESHOLD = 100

sensor = HCSR04(trigger_pin=19, echo_pin=21, echo_timeout_us=1000000)

trig_pin = Pin(19, Pin.OUT)
echo_pin = Pin(21, Pin.IN)
pin_18 = Pin(18, Pin.OUT) # buzzer pin

alarm_is_armed = False

# check if alarm was tripped
def proximity_sensor():
    global alarm_is_armed

    print('thread started')
    while True:
        time.sleep(0.5)
        distance = sensor.distance_mm()
        print(str(alarm_is_armed) + ', distance: ', distance)

        if distance < THRESHOLD and alarm_is_armed:
            print('TRIGGER')

            # send event to server
            addr = config.SERVER_ADDR + '/v1beta/client/device'
            body = { 'event': 'intruder', 'id': config.DEVICE_NAME }
            print('sending ' + event + ' event')
            try:
                urequests.post(addr, json=body)
            except:
                print('post failed')

            for i in range(5):
                time.sleep(1)
                pin_18.on()
                time.sleep(1)
                pin_18.off()


def server():
    global alarm_is_armed

    sta_if = network.WLAN(network.STA_IF)
    print(sta_if.ifconfig())

    addr = socket.getaddrinfo(URL, PORT)[0][-1]

    s = socket.socket()
    s.connect(addr)

    payload = 'GET /v1beta/event/device/' + config.DEVICE_NAME + ' HTTP/1.1\nHost: ' + HOST +'\n\n'
    print(payload)
    r = s.send(payload)

    _thread.start_new_thread(proximity_sensor, ())

    # TODO a lot of this code is nasty
    while True:

        # parse inputs
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

        if parsed['state'] == 'armed':
            alarm_is_armed = True
            print('alarm is armed')
        elif parsed['state'] == 'unarmed':
            alarm_is_armed = False
            print('alarm is unarmed')
        else:
            print('invalid alarm mode: ' + parsed['state'])

    s.close()

