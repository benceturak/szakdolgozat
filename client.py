import sys
import socket
import json
import time
import logging
sys.path.append('lib/')
sys.path.append('pyapi')
from totalstationclient import TotalStationClient
from leicatps1200 import LeicaTPS1200
from serialiface import SerialIface
from remotemeasureunit import RemoteMeasureUnit


iface = SerialIface("rs-232", "/dev/ttyUSB0")
mu = RemoteMeasureUnit(measureUnit = LeicaTPS1200())


ts = TotalStationClient('Leica', mu, iface)
ts.socketConnect(("192.168.0.50", 8081))
ts.InitStation()
ts.Trial('aaa')
ts.socketClose()


#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#msg = {'stid': None, 'cmd': 1001}
#msg = json.dumps(msg)
#sock.sendall(bytes('aaa', 'utf-8'))

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    # Connect to server and send data
    #sock.connect(("192.168.0.51", 8081))
    #i = 1

    #while True:

        #sock.sendall(bytes(str(i) + "aaaaa\n", "utf-8"))
        #i += 1

        # Receive data from the server and shut down
        #received = str(sock.recv(1024), "utf-8")

        #print(received)
        #time.sleep(2)


#print(sock.recv(1024))

#ts = TotalStationClient('teszt', 'Leica', sock)


#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #sock.connect(("192.168.0.51", 8081))

    #msg = {'stid': None, 'cmd': 1001}
    #msg = json.dumps(msg)
    #sock.sendall(msg.encode('ascii'))

    #sock.close()

#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #sock.connect(("192.168.0.51", 8081))
    #msg = {'stid': 0, 'cmd': 2001}
    #msg = json.dumps(msg)

    #sock.sendall(msg.encode('ascii'))

    # Receive data from the server and shut down
    #print(str(sock.recv(1024), "utf-8"))
