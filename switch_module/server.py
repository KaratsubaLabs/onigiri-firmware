PORT = 80
TIMEOUT = 3
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
    split = raw.lstrip("b'").rstrip("'").split()
    return {'method': split[0], 'path': split[1]}


def routes(c, req):

    if req['method'] == 'GET' and req['path'] == '/health':
        c.send('HTTP/1.1 200 OK\n\n')
    elif req['method'] == 'POST' and req['path'] == '/switch/on':
        handle_switch_set(True)
        c.send('HTTP/1.1 200 OK\n\n')
    elif req['method'] == 'POST' and req['path'] == '/switch/off':
        handle_switch_set(False)
        c.send('HTTP/1.1 200 OK\n\n')
    elif req['method'] == 'GET' and req['path'] == '/switch/state':
        state = handle_switch_state()
        c.send('HTTP/1.1 200 OK\n')
        c.send('Content-Type: application/json\n\n')
        c.send('{"state": %d}\n' % state)
    else:
        c.send('HTTP/1.1 404 NotFound\n\n')


def handle_switch_set(state):
    from machine import Pin

    pin_4 = Pin(4, Pin.OUT)
    if state:
        pin_4.on()
    else:
        pin_4.off()


def handle_switch_state():
    from machine import Pin

    pin_4 = Pin(4, Pin.OUT)
    print(pin_4.value())
    return pin_4.value()
