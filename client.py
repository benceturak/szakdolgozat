import socket
import json
import time

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect(("192.168.0.50", 8081))

    msg = {'stid': 0, 'cmd': 1001}
    msg = json.dumps(msg)
    #sock.sendall(msg.encode('ascii'))
    time.sleep(1)
    msg = {'stid': 0, 'cmd': 2001}
    msg = json.dumps(msg)

    sock.sendall(msg.encode('ascii'))

    # Receive data from the server and shut down
    #print(str(sock.recv(1024), "utf-8"))
