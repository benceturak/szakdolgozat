
import socketserver
import threading


#constants



class PiHandler(socketserver.StreamRequestHandler):

    def handle(self):
        print('aaaaa')
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = self.rfile.readline().strip()
        print("{} wrote:".format(self.client_address[0]))
        print(str(self.data, "utf-8"))
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(self.data.upper())

class ServerThread(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass
