import servo
import time

PORT = 80
TIMEOUT = 20
MAX_BODY_SIZE = 1024

LIGHT_IDLE_SERVO_ANGLE = 90
LIGHT_ON_SERVO_ANGLE = 45
LIGHT_OFF_SERVO_ANGLE = 135

servo.init(LIGHT_IDLE_SERVO_ANGLE)


def server():
    import socket
    import network

    sta_if = network.WLAN(network.STA_IF)
    print(sta_if.ifconfig())

    # TODO error handling
    addr = socket.getaddrinfo('0.0.0.0', PORT)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print('starting server on port:', 80)

    while True:
        c, addr = s.accept()
        c.settimeout(TIMEOUT)

        req = str(c.recv(MAX_BODY_SIZE))
        print('recieved connection from: ', addr)
        print(req)

        parsed_req = parse_http(req)
        routes(c, parsed_req)
        c.close()


def parse_http(raw):
    req_lines = raw.lstrip("b'").rstrip("'").split('\\r\\n')
    header = req_lines[0].split()

    body = ''
    if req_lines[-2] == '':
        body = req_lines[-1]

    return {'method': header[0], 'path': header[1], 'body': body}


def routes(c, req):
    if req['method'] == 'GET' and req['path'] == '/health':
        c.send('HTTP/1.1 200 OK\n\n')
    elif req['method'] == 'POST' and req['path'] == '/light/on':
        servo.set_angle(LIGHT_ON_SERVO_ANGLE)
        time.sleep(1)
        servo.set_angle(LIGHT_IDLE_SERVO_ANGLE)
        time.sleep(1)
        c.send('HTTP/1.1 200 OK\n\n')
    elif req['method'] == 'POST' and req['path'] == '/light/off':
        servo.set_angle(LIGHT_OFF_SERVO_ANGLE)
        time.sleep(1)
        servo.set_angle(LIGHT_IDLE_SERVO_ANGLE)
        time.sleep(1)
        c.send('HTTP/1.1 200 OK\n\n')
    else:
        c.send('HTTP/1.1 404 NotFound\n\n')
