

'''
API
'''

import urequests
import socket
import network
import ujson
import config
from hcsr04 import HCSR04
from machine import Pin

TIMEOUT = 20
MAX_BODY_SIZE = 4096

URL = '167.99.178.60'
PORT = 80
HOST = 'home.karatsubalabs.com'

THRESHOLD = 2

sensor = HCSR04(trigger_pin=18, echo_pin=19)

def server():

    while True:

        distance = sensor.distance_mm()
        print('distance: ', distance)

        if distance < THRESHOLD:
            print('TRIGGER')

            # addr = config.SERVER_ADDR + '/v1beta/client/device'
            # event = 'onPress' if state else 'onUnpress'
            # body = { 'event': event, 'id': config.DEVICE_NAME }
            # print('sending ' + event + ' event')
            # try:
            #     urequests.post(addr, json=body)
            # except:
            #     print('post failed')
            

    s.close()

    
