import time

PORT = 80
TIMEOUT = 20
MAX_BODY_SIZE = 1024

LIGHT_ON_SERVO_ANGLE = 45
LIGHT_OFF_SERVO_ANGLE = 135


def server():
    import socket
    import network

    sta_if = network.WLAN(network.STA_IF)
    print(sta_if.ifconfig())

    # TODO error handling
    # addr = socket.getaddrinfo('0.0.0.0', PORT)[0][-1]
    # s = socket.socket()
    # s.bind(addr)
    # s.listen(1)

    print('starting server on port:', 80)
    from machine import Pin
    import time
    leds = [
        Pin(23, Pin.OUT),
        Pin(25, Pin.OUT),
        Pin(26, Pin.OUT),
        Pin(27, Pin.OUT),
        Pin(32, Pin.OUT),
        Pin(33, Pin.OUT)
    ]
    ledsOutput = [0 for i in range(len(leds))]

    while True:
        # implement logic for getting diff leds from server
        # update ledsOutput

        ind = int(input("any led"))
        ledsOutput[ind] = not ledsOutput[ind]

        for ind in range(len(leds)):
            if ledsOutput[ind]:
                leds[ind].on()
            else:
                leds[ind].off()

        # c, addr = s.accept()
        # c.settimeout(TIMEOUT)

        # req = str(c.recv(MAX_BODY_SIZE))
        # print('recieved connection from: ', addr)
        # print(req.decode("utf-8"))

        # c.close()
