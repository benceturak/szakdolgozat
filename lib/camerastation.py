import sys
sys.path.append('ulyxes/pyapi/')
sys.path.append('lib/')
from totalstation import TotalStation
from serialiface import SerialIface
from camera import Camera
from camcalibparams import CamCalibParams
from steppermotor import StepperMotor
from imgprocess import ImgProcess
import numpy as np
import os
import cv2
import recognition as rec
from angle import Angle
import math
import time


class CameraStation(TotalStation, Camera):
    '''CameraStation class for TotalStation combinated with camera

        :param name:
        :param measureUnit:
        :param measureIface:
        :param cameraUnit:
        :param stepperMotorUnit:
        :param writerUnit:
        :param speed:
        :param halfSteps:
        :param affinParams:
        :param useImageCorrection:
    '''
    #constants
    FOCUS_CLOSER = 1
    FOCUS_FARTHER = 2

    #
    def __init__(self, name, measureUnit, measureIface, writerUnit = None):
        '''constructor
        '''
        TotalStation.__init__(self, name, measureUnit, measureIface, writerUnit)
        Camera.__init__(self, name, measureUnit, measureIface, writerUnit)
        #StepperMotor.__init__(self, stepperMotorUnit, speed, halfSteps)


        self._affinParams = None

        #self._useImageCorrection = useImageCorrection
        #initialize of focus

        #self._contrasts = [{'pos': self._position, 'contrast': -1}]

    def LoadAffinParams(self, name):
        self._affinParams = np.load(name)
        print(self._affinParams)
    def PicMes(self, photoName, targetType = None):
        '''Measure angles between the target and the optical axis
            :param photoName: name of the photo
            :target type: type of the target
            :params: horizontal (hz) and vertical (v) angle in dictionary
        '''

        ok = False
        while not ok:

            try:
                print(photoName)
                file = open(photoName, 'w+b')
                self.TakePhoto(file, (int(self._affinParams[0,3]), int(self._affinParams[1,3])))

                file.close()
                ang = self.GetAngles()


                img = cv2.imread(photoName, 1)
                picCoord = rec.recogChessPattern(img)
                print(picCoord)
                ok = True
            except:
                pass

        print('ok')

        img[int(picCoord[1]),int(picCoord[0])] = [0,255,255]

        cv2.imwrite(photoName, img)
        angles = {}
        angles['hz'] = Angle(1/math.sin(ang['v'].GetAngle('RAD'))*(self._affinParams[0,1]*(picCoord[0] - self._affinParams[0,0]) + self._affinParams[0,2]*(picCoord[1] - self._affinParams[1,0])))
        angles['v'] = Angle(self._affinParams[1,1]*(picCoord[0] - self._affinParams[0,0]) + self._affinParams[1,2]*(picCoord[1] - self._affinParams[1,0]))


        return angles

    def GetAbsAngles(self, targetType = None):

        t = time.localtime()
        picName = str(t.tm_year) + '_' + str(t.tm_mon) + '_' + str(t.tm_mday) + '_' + str(t.tm_hour) + '_' + str(t.tm_min) + '_' + str(t.tm_sec) + '.png'

        corr = self.PicMes(picName)
        ang = self.GetAngles()

        angles = {}
        angles['hz'] = ang['hz'] - corr['hz']
        angles['v'] = ang['v'] - corr['v']
        i = 0

        print('hz:', corr['hz'].GetAngle('SEC'))
        print('v:', corr['v'].GetAngle('SEC'))

        while corr['hz'].GetAngle('SEC') > 6 or corr['v'].GetAngle('SEC') > 6:



            self.Move(angles['hz'], angles['v'])

            corr = self.PicMes(picName)
            ang = self.GetAngles()
            print('hz:', corr['hz'].GetAngle('SEC'))
            print('v:', corr['v'].GetAngle('SEC'))
            angles = {}
            angles['hz'] = ang['hz'] - corr['hz']
            angles['v'] = ang['v'] - corr['v']
            print(i)
            i += 1
        return angles

    def FollowTarget(self):
        t = time.localtime()
        picName = str(t.tm_year) + '_' + str(t.tm_mon) + '_' + str(t.tm_mday) + '_' + str(t.tm_hour) + '_' + str(t.tm_min) + '_' + str(t.tm_sec) + '.png'

        i = 0

        while True:

            corr = self.PicMes(picName)
            ang = self.GetAngles()
            print('hz:', corr['hz'].GetAngle('SEC'))
            print('v:', corr['v'].GetAngle('SEC'))
            angles = {}
            angles['hz'] = ang['hz'] - corr['hz']
            angles['v'] = ang['v'] - corr['v']
            print(i)
            i += 1
            if abs(corr['hz'].GetAngle('SEC')) > 6 or abs(corr['v'].GetAngle('SEC')) > 6 :
                self.Move(angles['hz'], angles['v'])


        return angles

    def _picMeasure(self, numOfTargets = 1, checkPic = True,  savePic = True):
        picName = ''
        self.takePhoto(picName)

        img = ImgProcess(picName)

        targets = img.findTargets()

        if checkPic:
            check = cv2.circle(img.img,(int(x), int(y)), 10, (0,0,255), 1)
            cv2.imshow('check', check)


        if targets.shape[0] > numOfTargets:
            print('Warning! More targets are found!')
        else:
            pass
        return x, y


    def targetOn(self):
        '''target on method
        '''
        pass

    def __del__(self):
        '''destructor
        '''
        pass
        #StepperMotor.__del__(self)
