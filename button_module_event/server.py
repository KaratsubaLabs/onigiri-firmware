

'''
API
'''

import urequests
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


pin_18 = Pin(18, Pin.IN, Pin.PULL_UP)
def button_state():
    return not pin_18.value()

def server():

    state = button_state()
    while True:
        new_state = button_state()
        if new_state != state:
            state = new_state

            addr = config.SERVER_ADDR + '/v1beta/client/device'
            event = 'onPress' if state else 'onUnpress'
            body = { 'event': event, 'id': config.DEVICE_NAME }
            print('sending ' + event + ' event')
            try:
                urequests.post(addr, json=body)
            except:
                print('post failed')

            

    s.close()

    
