#import total
from totalstation import TotalStation
from serialiface import SerialIface
from leicatps1200 import LeicaTPS1200
from leicameasureunit import LeicaMeasureUnit
import socketserver
import json

#iface = SerialIface('test', '/dev/ttyUSB0')
#ts = TotalStation('test', LeicaTPS1200(), iface)

class TotalStationRequestHandler(socketserver.StreamRequestHandler):
    '''TCP request handler for total stations remote controll

    '''

    CMD_CODES = {
    'NEW_TS': 1001,
    'NEW_CS': 1002,
    'MEASURE': 2001
    }

    def handle(self):
        print(self.server.stations)
        msg = self.getRequest()
        self.process(msg)


        #print("{} wrote:".format(self.client_address[0]))
        #print(self.data.decode('ascii'))
    def setNewStation(self, station):
        if isinstance(station, TotalStation):
            self.server.stations.append(station)
    def getRequest(self):
        return json.loads(self.rfile.readline().strip().decode('ascii'))
    def process(self, msg):
        print(msg)
        if msg['cmd'] == self.CMD_CODES['NEW_TS']:
            iface = SerialIface('rs-232', '/dev/ttyUSB0', baud=19200)
            ts = TotalStation('test', LeicaMeasureUnit(), iface)
            self.setNewStation(ts)
            ans = ''
        elif msg['cmd'] == self.CMD_CODES['MEASURE']:
            self.server.stations[0].Measure()
            ans = ''
        return ans



    #def sendAnswer(self):
        #pass
    #def processRequest(self):
        #pass
