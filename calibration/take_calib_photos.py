import sys
sys.path.append('../ulyxes/pyapi')
sys.path.append('../lib/')
from camerastation import CameraStation
from totalstation import TotalStation
from remotemeasureunit  import RemoteMeasureUnit
from tcpiface import TCPIface
from angle import Angle
import math
import time
import numpy as np
import recognition as rec
import cv2


mu = RemoteMeasureUnit()

iface = TCPIface('test', ('192.168.0.51', 8081), timeout=25)

ts = CameraStation('test', mu, iface)
first = {}
last = {}
print('Mark out the calibration area')
input('Target on the top-left corner')
first = ts.GetAngles()
#first['hz'] = Angle('104-19-46', 'DMS')
#first['v'] = Angle('89-28-53', 'DMS')
input('Target on the bottom-right corner')
last = ts.GetAngles()
#last['hz'] = Angle('104-52-02', 'DMS')
#last['v'] = Angle('89-55-18', 'DMS')
#last = ts.GetAngles()


input('Press enter to start calibration')

steps = 3


hz = [first['hz']]
v = [first['v']]

r = {}
r['hz'] = (last['hz'].GetAngle('RAD') - first['hz'].GetAngle('RAD'))/2
r['v'] = (last['v'].GetAngle('RAD') - first['v'].GetAngle('RAD'))/2

for i in range(1, steps - 1):
    hz.append(first['hz'] + Angle(i * r['hz'], 'RAD'))
    v.append(first['v'] + Angle(i * r['v'], 'RAD'))

hz.append(last['hz'])
v.append(last['v'])


face1 = np.empty((0,4))

face2 = np.empty((0,4))


#ts.TakePhoto('calib_images/hz'+str(int(hz2.GetAngle('SEC')))+'v'+str(int(v2.GetAngle('SEC')))+'.png')


for vv in v:
    for hzz in hz:

        ts.Move(hzz, vv)
        ans = 'n'
        while ans == 'n':
            try:
                angles = ts.GetAngles()


                name = 'hz'+angles['hz'].GetAngle('DMS')+'v'+angles['v'].GetAngle('DMS')+'.png'
                pic = ts.TakePhoto(name, 'png')
                f = open(name, 'w+b')
                f.write(pic)
                f.close()

                img = cv2.imread(name, 1)

                picCoord = rec.recog(img)
                line = [[angles['hz'].GetAngle('RAD'), angles['v'].GetAngle('RAD'), picCoord[0], picCoord[1]]]
                print(line)
                ans = 'y'
            except:
                ans = 'n'
        face1 = np.append(face1, line , axis=0)
print(face1)
input('Turn station to second face')
for vv in v:
    for hzz in hz:

        ts.Move(hzz + Angle(180, 'DEG'), Angle(360, 'DEG') - vv)
        ans = 'n'
        while ans == 'n':
            try:
                angles = ts.GetAngles()


                name = 'hz'+angles['hz'].GetAngle('DMS')+'v'+angles['v'].GetAngle('DMS')+'.png'
                pic = ts.TakePhoto(name, 'png')
                f = open(name, 'w+b')
                f.write(pic)
                f.close()

                img = cv2.imread(name, 1)

                picCoord = rec.recog(img)
                line = [[angles['hz'].GetAngle('RAD'), angles['v'].GetAngle('RAD'), picCoord[0], picCoord[1]]]
                print(line)
                ans = 'y'
            except:
                ans = 'n'
        face2 = np.append(face2, line, axis=0)

calib = np.append(face1, face2, axis=0)
np.save('calibparams.npy', calib)
#img = cv2.imread(f, 1)
#
#print(aaa)




#print(face1)
#time.sleep(3)



#ts.Measure()
