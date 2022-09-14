
PORT = 80
TIMEOUT = 3
MAX_BODY_SIZE = 1024

import lcd

lcd.init()


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
    return {
        'method': split[0],
        'path': split[1]
    }


def routes(c, req):
    if req['method'] == 'GET' and req['path'] == '/health':
        c.send('HTTP/1.1 200 Ok\n')
    elif req['method'] == 'POST' and req['path'] == '/lcd':
        lcd.clear_screen()
        lcd.set_line(lcd.LINE_ONE)
        lcd.display("hello!")
    else:
        c.send('HTTP/1.1 404 NotFound\n')

