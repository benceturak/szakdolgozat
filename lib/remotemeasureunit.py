import sys
import json
sys.path.append('../ulyxes/pyapi/')
import re
from measureunit import MeasureUnit
from angle import Angle
import logging
import json


class RemoteMeasureUnit(MeasureUnit):


    codes = {
        'TRIAL': -1
    }

    def __init__(self, name = 'REMOTE STATION', typ = 'VIRTUAL'):
        """ Constructor to remote total station
        """
        super(RemoteMeasureUnit, self).__init__(name, typ)
    def Result(self, msgs, anss):
        """ Parse answer from message

            :param msgs: messages sent to server
            :param anss: aswers got from server
            :returns: dictionary
        """
        msgList = re.split('\|', msgs)
        ansList = re.split('\|', anss)
        res = {}
        for msg, ans in zip(msgList, ansList):
            # get command id form message
            msgBufflist = json.loads(msg)

            cmd = msgBufflist['cmd']

            # get error code from answer
            ansBufflist = json.loads(ans)
            print(ans)
            try:
                errCode = int(ansBufflist['err'])
                if cmd == self.codes['TRIAL']:
                    res['param'] = ansBufflist['params']['param1']
            except ValueError:
                errCode = -1   # invalid answer
            except IndexError:
                errCode = -2   # instrument off?
            if errCode != 0:
                logging.error(" error from instrument: %d", errCode)
                res['errorCode'] = errCode
                #if not errCode in (1283, 1284, 1285, 1288): # do not stop if accuracy is not perfect
        return res

    def TrialMsg(self, param):
        params = {'param1': param}
        msg = {'stid': None, 'cmd': self.codes['TRIAL'], 'params': params}
        return json.dumps(msg)

    def InitStationMsg(self):
        params = {'measureUnit': repr(self)}
        msg = {'stid': None, 'cmd': self.codes['NEW_TS'], 'params': params}
        return json.dumps(msg)

    def __repr__(self):
        return type(self).__name__+'(name="{0:s}", typ="{1:s}", measuerUnit="{2:s}")'.format(str(self.name), str(self.typ), repr(self.measureUnit))
