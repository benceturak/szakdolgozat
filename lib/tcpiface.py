import sys
sys.path.append('../ulyxes/pyapi/')
from iface import Iface
import socket
import logging
import re

class TCPIface(Iface):

    def __init__(self, name, address, bufSize = 1024, timeout=15):
        """ Constructor for TCP socket interface
        """
        super(TCPIface, self).__init__(name)
        # open serial port
        self.sock = None
        self.bufSize = None

        self.Open(address, bufSize, timeout)
    def __del__(self):
        """ Destructor for TCP socket interface
        """
        self.Close()
    def Open(self, address, bufSize = 1024, timeout=15):
        """ Open TCP socket
        """
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect(address)
            self.sock.settimeout(timeout)
            self.bufSize = bufSize
            self.opened = True
            self.state = self.IF_OK
        except:
            self.opened = False
            self.state = self.IF_ERROR
            logging.error(" cannot open TCP socket")
    def Close(self):
        """ Close TCP socket
        """
        try:
            self.sock.close()
            self.opened = False
            self.state = self.IF_OK
        except:
            self.state = self.IF_ERROR
            logging.error(" cannot close TCP socet")
    def GetLine(self, bufSize = None):
        """ read from TCP interface until end of line

        :returns: line read from TCP (str) or empty string on timeout or error, state is set also
        """
        if self.sock is None or not self.opened or self.state != self.IF_OK:
            logging.error(" TCP socket not opened")
            return None
        # read answer till end of line

        ans = b''
        a = b''
        try:
            if bufSize != None:

                a = self.sock.recv(1024)
                ans += a
                while sys.getsizeof(ans) < bufSize + 17:
                    l = sys.getsizeof(ans)
                    a = self.sock.recv(1024)
                    ans += a
            else:
                a = self.sock.recv(1)
                ans += a
                while a != b'\n':
                    a = self.sock.recv(1)
                    ans += a

        except Exception as e:
            #self.state = self.IF_READ
            logging.error(" cannot read TCP socket")
        if ans == b'':
            # timeout exit loop
            #self.state = self.IF_TIMEOUT
            logging.error(" timeout on TCP socket")
        # remove end of line
        logging.debug(" message got: %s", ans)
        ans = ans.strip(b'\n')
        return ans

    def PutLine(self, msg):
        """ send message through the TCP socket

            :param msg: message to send (str)
            :returns: 0 - on OK, -1 on error or interface is in error state
        """
        # do nothing if interface is in error state
        if self.sock is None or not self.opened or self.state != self.IF_OK:
            logging.error(" TCP socket not opened or in error state")
            return -1
        # add CR/LF to message end
        w = -1 * len('\n')
        if (msg[w:] != '\n'):
            msg += '\n'
        # remove special characters
        msg = msg.encode('ascii', 'ignore')
        # send message to serial interface
        logging.debug(" message sent: %s", msg)
        try:
            self.sock.send(msg)
        except:
            self.state = self.IF_WRITE
            logging.error(" cannot write serial line")
            return -1
        return 0

    def Send(self, msg):
        """ send message to TCP socket and read answer

            :param msg: message to send, it can be multipart message separated by '|' (str)
            :returns: answer from server (str)
        """
        msglist = re.split("\|", msg)
        res = b''
        #sending
        for m in msglist:
            if self.PutLine(m) == 0:
                res += self.GetLine() + b"|"
        if res.endswith(b"|"):
            res = res[:-1]
        res = res.decode('ascii')
        return res

if __name__ == "__main__":
    a = TCPIface('test', ('192.168.0.50', 8081), 1024, 15)
    print (a.GetName())
    print (a.GetState())
    print (a.Send('%R1Q,2008:1,0'))
