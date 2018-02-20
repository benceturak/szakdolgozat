import pilib.piserver
import socketserver
import threading

if __name__ == "__main__":


    server = pilib.piserver.ServerThread(('192.168.0.50', 8081), pilib.piserver.PiHandler)

    thread = threading.Thread(target=server.serve_forever)
    thread.start()
