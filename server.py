import sys
sys.path.append('pyapi')
sys.path.append('lib')
from totalstationrequesthandler import TotalStationRequestHandler

import socketserver
import threading

class StationServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass):
        socketserver.TCPServer.__init__(self, server_address, RequestHandlerClass)
        self.stations = []

if __name__ == "__main__":


    server = StationServer(('192.168.0.50', 8081), TotalStationRequestHandler)

    server.serve_forever()

    #thread = threading.Thread(target=server.serve_forever)
    #thread.start()
