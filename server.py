
PORT = 80
TIMEOUT = 3
MAX_BODY_SIZE = 1024

def server():
    import socket
    
    # TODO error handling
    addr = socket.getaddrinfo('0.0.0.0', PORT)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("starting server on port:", 80)

    while True:
        c, addr = s.accept()
        c.settimeout(TIMEOUT)

        req = str(c.recv(MAX_BODY_SIZE))
        print("recieved connection from: ", addr)
        print(req)
        c.send('HTTP/1.1 200 Ok\n')
        c.send('Content-Type: application/json\n')
        c.close()

