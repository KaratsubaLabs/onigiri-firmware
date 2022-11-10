import time
import motor

PORT = 80
TIMEOUT = 20
MAX_BODY_SIZE = 1024


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
    elif req['method'] == 'POST' and req['path'] == '/curtain/open':
        motor.motor_left()
        c.send('HTTP/1.1 200 OK\n\n')
    elif req['method'] == 'POST' and req['path'] == '/curtain/close':
        motor.motor_right()
        c.send('HTTP/1.1 200 OK\n\n')
    elif req['method'] == 'POST' and req['path'] == '/curtain/stop':
        motor.motor_stop()
        c.send('HTTP/1.1 200 OK\n\n')
    else:
        c.send('HTTP/1.1 404 NotFound\n\n')
