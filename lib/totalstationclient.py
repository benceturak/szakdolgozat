import sys
sys.path.append('../ulyxes/pyapi/')
from leicatps1200 import LeicaTPS1200
from totalstation import TotalStation
from stationcommands import StationCommands
import logging
import socket
import json



class TotalStationClient(TotalStation):

    def Trial(self, param1):

        msg = self.measureUnit.TrialMsg(param1)
        print(msg)
        return self._process(msg)
