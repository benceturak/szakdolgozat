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
        'SWITCHON': 111,
        'SWITCHOFF': 112,
        'SETPC': 2024,
        'GETPC': 2023,
        'INSTRNO': 5003,
        'INSTRNAME': 5004,
        'INTTEMP': 5011,
        'SETATR': 9018,
        'GETATR': 9019,
        'SETLOCK': 9020,
        'GETLOCK': 9021,
        'LOCKIN': 9013,
        'SETATMCORR': 2028,
        'GETATMCORR': 2029,
        'SETREFCORR': 2030,
        'GETREFCORR': 2031,
        'GETSTN': 2009,
        'SETSTN': 2010,
        'SETEDMMODE': 2020,
        'GETEDMMODE': 2021,
        'SETORI': 2113,
        'MOVE': 9027,
        'MEASURE': 2008,
        'GETMEASURE': 2108,
        'MEASUREANGDIST': 17017,
        'COORDS': 2082,
        'GETANGLES': 2003,
        'CHANGEFACE': 9028,
        'CLEARDIST': 2082,
        'SETSEARCHAREA': 9043,
        'POWERSEARCH': 9052,
        'SEARCHNEXT': 9051,
        'SETREDLASER': 1004,
        'GETPT': 17009,
        'SETPT': 17008,
        'GETSPIRAL': 9040,
        'SETSPIRAL': 9041,
        'SEARCHTARGET': 17020,
        'TRIAL': -1
    }

    edmModes = {'STANDARD': 0, 'PRECISE': 1, 'FAST': 2, 'TRACKING': 3,
                'AVERAGING': 4, 'FASTTRACKING': 5}


    edmProg = {'STOP': 0, 'DEFAULT': 1, 'TRACKING': 2, 'CLEAR': 3}

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

            # get error code from answer
            ansBufflist = json.loads(ans)
            try:
                errCode = int(ansBufflist['err'])

                params = ansBufflist['params']
                for key, val in params.items():
                    res[key] = eval(val)
            except ValueError:
                errCode = -1   # invalid answer
            except IndexError:
                errCode = -2   # instrument off?
            if errCode != 0:
                logging.error(" error from instrument: %d", errCode)
                res['errorCode'] = errCode
                #if not errCode in (1283, 1284, 1285, 1288): # do not stop if accuracy is not perfect
        return res
    @staticmethod
    def execCmd(ts, msg):

        print(b'---------')
        msgBufflist = json.loads(msg.decode('ascii'))

        cmd = msgBufflist['cmd']
        params = msgBufflist['params']
        print(params)

        try:
            err = 0
            if cmd == RemoteMeasureUnit.codes['GETMEASURE']:
                res = ts.GetMeasure(params['wait'], params['incl'])
            elif cmd == RemoteMeasureUnit.codes['MEASUREANGDIST']:
                res = ts.MeasureDistAngMsg(params['prg'])
            elif cmd == RemoteMeasureUnit.codes['GETPC']:
                res = ts.GetPc(params['prg'])
            elif cmd == RemoteMeasureUnit.codes['GETPT']:
                res = ts.GetPrismType()
            elif cmd == RemoteMeasureUnit.codes['GETATR']:
                res = ts.GetATR()
            elif cmd == RemoteMeasureUnit.codes['GETLOCK']:
                res = ts.GetLock()
            elif cmd == RemoteMeasureUnit.codes['GETATMCORR']:
                res = ts.GetAtmCorr()
            elif cmd == RemoteMeasureUnit.codes['GETREFCORR']:
                res = ts.GetRefCorr()
            elif cmd == RemoteMeasureUnit.codes['GETSTN']:
                res = ts.GetStation()
            elif cmd == RemoteMeasureUnit.codes['GETEDMMODE']:
                res = ts.GetEDMMode()
            elif cmd == RemoteMeasureUnit.codes['COORDS']:
                res = ts.Coords(params['wait'], params['incl'])
            elif cmd == RemoteMeasureUnit.codes['GETANGLES']:
                res = ts.GetAngles()
            elif cmd == RemoteMeasureUnit.codes['GETSPIRAL']:
                res = ts.GetSpiral()
            elif cmd == RemoteMeasureUnit.codes['SETSPIRAL']:
                res = ts.SetSpiral(params['dRangeHz'], params['dRangeV'])
            elif cmd == RemoteMeasureUnit.codes['INSTRNO']:
                res = ts.GetInstrumentNo()
            elif cmd == RemoteMeasureUnit.codes['INSTRNAME']:
                res = ts.GetInstrumentName()
            elif cmd == RemoteMeasureUnit.codes['INTTEMP']:
                res = ts.GetInternalTemperature()
            elif cmd == RemoteMeasureUnit.codes['SWITCHOFF']:
                res = ts.SwitchOff()
            elif cmd == RemoteMeasureUnit.codes['SWITCHON']:
                res = ts.SwitchOn(params['mode'])
            elif cmd == RemoteMeasureUnit.codes['SEARCHTARGET']:
                res = ts.SearchTarget()
            elif cmd == RemoteMeasureUnit.codes['CHANGEFACE']:
                res = ts.ChangeFace()
            elif cmd == RemoteMeasureUnit.codes['SETORI']:
                res = ts.SetOri(params['ori'])
            elif cmd == RemoteMeasureUnit.codes['SETEDMMODE']:
                res = ts.SetEDMMode(params['mode'])
            elif cmd == RemoteMeasureUnit.codes['SETSTN']:
                res = ts.SetStation(params['e'], params['n'], params['z'], params['ih'])
            elif cmd == RemoteMeasureUnit.codes['SETREFCORR']:
                res = ts.SetRefCorr(params['status'], params['earthRadius'], params['refracticeScale'])
            elif cmd == RemoteMeasureUnit.codes['SETATMCORR']:
                res = ts.SetAtmCorr(params['valueOfLambda'], params['pres'], params['dry'], params['wet'])
            elif cmd == RemoteMeasureUnit.codes['LOCKIN']:
                res = ts.LockIn()
            elif cmd == RemoteMeasureUnit.codes['SETLOCK']:
                res = ts.SetLock(params['lock'])
            elif cmd == RemoteMeasureUnit.codes['SETATR']:
                res = ts.SetATR(params['atr'])
            elif cmd == RemoteMeasureUnit.codes['SETPT']:
                res = ts.SetPrismType(params['typ'])
            elif cmd == RemoteMeasureUnit.codes['MEASURE']:
                res = ts.Measure(params['prg'], params['incl'])
            elif cmd == RemoteMeasureUnit.codes['GETMEASURE']:
                res = ts.GetMeasure()
            elif cmd == RemoteMeasureUnit.codes['MOVE']:
                res = ts.Move(Angle(params['hz']), Angle(params['v']))
            elif cmd == RemoteMeasureUnit.codes['TRIAL']:
                res = ts.Trial(params['param1'])
        except:
            err = 1
        res['err'] = err

        for key, val in res.items():
            res[key] = repr(val)

        return json.dumps(res).encode('ascii')

    def SetPcMsg(self, pc):
        """ Set prism constant

            :param pc: prism constant [mm]
            :returns: set prism constant message
        """

        params = {'pc': pc}
        msg = {'cmd': self.codes['SETPC'], 'params': params}
        return json.dumps(msg)

    def GetPcMsg(self):
        """ Get prism constant

            :returns: get prism constant message
        """
        params = {}
        msg = {'cmd': self.codes['GETPC'], 'params': params}
        return json.dumps(msg)

    def SetPrismTypeMsg(self, typ):
        """ Set prism type

            :param typ: prism type (0/1/2/3/4/5/6/7 round/mini/tape/360/user1/user2/user3/360 mini)
        """
        params = {'typ': typ}
        msg = {'cmd': self.codes['SETPT'], 'params': params}
        return json.dumps(msg)

    def GetPrismTypeMsg(self):
        """ Get prism type

            :returns: prism type (0/1/2/3/4/5/6/7 round/mini/tape/360/user1/user2/user3/360 mini)
        """
        params = {}
        msg = {'cmd': self.codes['GETPT'], 'params': params}
        return json.dumps(msg)

    def SetATRMsg(self, atr):
        """ Set ATR status on/off

            :param atr: 0/1 = off/on
            :returns: set atr message string
        """
        params = {'atr': atr}
        msg = {'cmd': self.codes['SETATR'], 'params': params}
        return json.dumps(msg)

    def GetATRMsg(self):
        """ Get ATR status

            :returns: get atr message
        """
        params = {}
        msg = {'cmd': self.codes['GETATR'], 'params': params}
        return json.dumps(msg)

    def SetLockMsg(self, lock):
        """ Set Lock status

            :param lock: 0/1 = off/on
            :returns: set lock status message
        """
        params = {'lock', lock}
        msg = {'cmd': self.codes['SETLOCK'], 'params': params}
        return json.dumps(msg)

    def GetLockMsg(self):
        """ Get Lock status

            :returns: get lock status message
        """
        params = {}
        msg = {'cmd': self.codes['GETLOCK'], 'params': params}
        return json.dumps(msg)

    def LockInMsg(self):
        """ Activate lock

            :returns: active lock message
        """
        params = {}
        msg = {'cmd': self.codes['LOCKIN'], 'params': params}
        return json.dumps(msg)

    def SetAtmCorrMsg(self, valueOfLambda, pres, dry, wet):
        """ Set atmospheric correction settings

            :param valueOfLambda: Constant for the instrument not changeable, use GetAtmCorr to get value
            :param pres: pressure value
            :param dry: dry temperature
            :param wet: wet temperature
            :returns: set atmospheric correction message
        """
        params = {'valueOfLambda': valueOfLambda, 'pres': pres, 'dry': dry, 'wet': wet}
        msg = {'cmd': self.codes['SETATMCORR'], 'params': params}
        return json.dumps(msg)

    def GetAtmCorrMsg(self):
        """ Get atmospheric correction settings

            :returns: iget atmospheric settings message
        """
        params = {}
        msg = {'cmd': self.codes['GETATMCORR'], 'params': params}
        return json.dumps(msg)

    def SetRefCorrMsg(self, status, earthRadius, refracticeScale):
        """ Set refraction correction settings

            :param status: 0/1 = off/on
            :param earthRadius: radius ot the Earth
            :param refracticeScale: refractice scale
            :returns: set refraction message
        """
        params = {'status': status, 'earthRadius': earthRadius, 'refracticeScale': refracticeScale}
        msg = {'cmd': self.codes['SETREFCORR'], 'params': params}
        return json.dumps(msg)

    def GetRefCorrMsg(self):
        """ Get refraction correction setting

            :returns: get refraction correction message

        """
        params = {}
        msg = {'cmd': self.codes['GETREFCORR'], 'params': params}
        return json.dumps(msg)

    def SetStationMsg(self, e, n, z, ih=0.0):
        """ Set station coordinates

            :param e: easting
            :param n: northing
            :param z: elevation
            :param ih: instrument height (optional, default 0)
            :returns: set station coordinates message
        """
        params = {'e': e, 'n': n, 'z': z, 'ih': ih}
        msg = {'cmd': self.codes['SETSTN'], 'params': params}
        return json.dumps(msg)

    def GetStationMsg(self):
        """ Get station coordinates

        :returns: get station coordinates message

        """
        params = {}
        msg = {'cmd': self.codes['GETSTN'], 'params': params}
        return json.dumps(msg)

    def SetEDMModeMsg(self, mode):
        """ Set EDM mode

            :param mode: string name
            :returns: set edm mode message
        """
        if type(mode) is str:
            imode = self.edmModes[mode]
        else:
            imode = mode
        params = {'mode': imode}
        msg = {'cmd': self.codes['SETEDMMODE'], 'params': params}
        return json.dumps(msg)

    def GetEDMModeMsg(self):
        """ Get EDM mode

            :returns: get edm mode message
        """
        params = {}
        msg = {'cmd': self.codes['GETEDMMODE'], 'params': params}
        return json.dumps(msg)

    def SetOriMsg(self, ori):
        """ Set orientation angle

            :param ori: bearing of direction (Angle)
            :returns: 0 or error code

        """
        params = {'ori': ori.GetAngle('RAD')}
        msg = {'cmd': self.codes['SETORI'], 'params': params}
        return json.dumps(msg)

    def MoveMsg(self, hz, v, atr = 0):
        """ Rotate instrument to direction with ATR or without ATR

            :param hz: horizontal direction (Angle)
            :param v: zenith angle (Angle)
            :param atr: 0/1 atr off/on, default off
            :returns: rotate message

        """
        params = {'hz': hz.GetAngle('RAD'), 'v': v.GetAngle('RAD'), 'atr': atr}
        msg = {'cmd': self.codes['MOVE'], 'params': params}
        return json.dumps(msg)

    def MeasureMsg(self, prg=1, incl=0):
        """ Measure distance

            :param prg: measure program 1/2/3/... = default/track/clear..., optional (default 1, mode set before)
            :param incl: inclination calculation - 0/1/2 = measure always (slow)/calculate (fast)/automatic, optional (default 0)

            :returns: measure message
        """
        params = {'prg': prg, 'incl': incl}
        msg = {'cmd': self.codes['MEASURE'], 'params': params}
        return json.dumps(msg)

    def GetMeasureMsg(self, wait=15000, incl=0):
        """ Get measured distance

            :param wait: time in ms, optional (default 15000), it must be greater than 12000, the default on the instrument
            :param incl: inclination calculation - 0/1/2 = measure always (slow)/calculate (fast)/automatic, optional (default 0)
            :returns: get simple measurement message
        """

        params = {'wait': wait, 'incl': incl}
        msg = {'cmd': self.codes['GETMEASURE'], 'params': params}
        return json.dumps(msg)

    def MeasureDistAngMsg(self, prg):
        """ Measure angles and distance

            :param prg: EDM program
            :returns: measure angle distance message

        """
        if type(prg) is str:
            prg = self.edmProg[prg]

        params = {'prg': prg}
        msg = {'cmd': self.codes['MEASUREANGDIST'], 'params': params}
        return json.dumps(msg)

    def CoordsMsg(self, wait=15000, incl=0):
        """ Get coordinates

            :param wait: wait-time in ms, optional (default 15000), it must be greater than 12000, the default on instrument
            :param incl: inclination calculation - 0/1/2 = measure always (slow)/calculate (fast)/automatic, optional (default 0)
            :returns: get coordinates message
        """
        params = {'wait': wait, 'incl': incl}
        msg = {'cmd': self.codes['COORDS'], 'params': params}
        return json.dumps(msg)

    def GetAnglesMsg(self):
        """ Get angles

                :returns: get angles message
        """
        params = {}
        msg = {'cmd': self.codes['GET_ANGLES'], 'params': params}
        return json.dumps(msg)

    def ClearDistanceMsg(self):
        """ Clearing distance

                :returns: clear distance message

        """
        return self.MeasureMsg(self, 3)

    def ChangeFaceMsg(self):
        """ Change face

            :returns: change face message
        """
        params = {}
        msg = {'cmd': self.codes['CHANGEFACE'], 'params': params}
        return json.dumps(msg)

    def GetSpiralMsg(self):
        """ Get search spiral parameters

            :returns: get spiral message
        """
        params = {}
        msg = {'cmd': self.codes['GETSPIRAL'], 'params': params}
        return json.dumps(msg)

    def SetSpiralMsg(self, dRangeHz, dRangeV):
        """ Set search priral parameters

            :param dRangeHz: horizontal range of search (Angle)
            :param dRangeV: vertical range of search (Angle)
            :returns: set search spiral message
        """
        params = {'dRangeHz': dRangeHz, 'dRangeV': dRangeV}
        msg = {'cmd': self.codes['SETSPIRAL'], 'params': params}
        return json.dumps(msg)

    def SearchTargetMsg(self):
        """ Search target using user spiral

            :returns: Search target message
        """
        params = {}
        msg = {'cmd': self.codes['SEARCHTARGET'], 'params': params}
        return json.dumps(msg)

    def SwitchOnMsg(self, mode=1):
        """ Switch on instrument or wake up and change to remote mode

            :param mode: startup mode 0/1 local/remote
            :returns: switch on message
        """
        params = {'mode': mode}
        msg = {'cmd': self.codes['SWITCHON'], 'params': params}
        return json.dumps(msg)

    def SwitchOffMsg(self):
        """ Switch off instrument

        """
        params = {}
        msg = {'cmd': self.codes['SWITCHOFF'], 'params': params}
        return json.dumps(msg)

    def GetInstrumentNoMsg(self):
        """ Get instrument factory number

            :returns: get instrument factory number message
        """
        params = {}
        msg = {'cmd': self.codes['INSTRNO'], 'params': params}
        return json.dumps(msg)

    def GetInstrumentNameMsg(self):
        """ Get instrument name

            :returns: get instrument name
        """
        params = {}
        msg = {'cmd': self.codes['INSTRNAME'], 'params': params}
        return json.dumps(msg)

    def GetInternalTemperatureMsg(self):
        """ Get instrument internal temperature

            :returns: instrument internal temperature
        """
        params = {}
        msg = {'cmd': self.codes['INTTEMP'], 'params': params}
        return json.dumps(msg)

    def TrialMsg(self, param):
        params = {'param1': param}
        msg = {'cmd': self.codes['TRIAL'], 'params': params}
        return json.dumps(msg)

    def __repr__(self):
        return type(self).__name__+'(name="{0:s}", typ="{1:s}", measuerUnit="{2:s}")'.format(str(self.name), str(self.typ), repr(self.measureUnit))
