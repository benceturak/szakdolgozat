import sys
sys.path.append('ulyxes/pyapi')
sys.path.append('lib/')
from camerastation import CameraStation
from totalstation import TotalStation
from remotemeasureunit  import RemoteMeasureUnit
from tcpiface import TCPIface
from serialiface import SerialIface
from leicatps1200 import LeicaTPS1200
from picameraunit import PiCameraUnit
from angle import Angle
import math
import time
import numpy as np
import recognition as rec
import cv2


mu = RemoteMeasureUnit()
iface = TCPIface('test', ('192.168.1.102', 8081), timeout=25)

class CameraStationUnit(PiCameraUnit, LeicaTPS1200): pass

#mu = CameraStationUnit()
#iface = SerialIface('test', '/dev/ttyUSB0')

ts = CameraStation('test', mu, iface)

#ts.Move(Angle('104-19-46', 'DMS'), Angle('89-28-53', 'DMS'))

ts.LoadAffinParams('calibration/aparams_400_500.npy')

angs = ts.FollowTarget()
print(angs['hz'].GetAngle('DMS'))
print(angs['v'].GetAngle('DMS'))
print(angs)
print('-----------------')

#ts.Move(angs['hz'], angs['v'])

#angs = ts.GetAbsAngles()
#print(angs)
