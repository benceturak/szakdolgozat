import sys
sys.path.append('ulyxes/pyapi/')
sys.path.append('lib/')
from totalstation import TotalStation
from serialiface import SerialIface
from camera import Camera
from camcalibparams import CamCalibParams
from steppermotor import StepperMotor
from picamera import PiCamera
import numpy as np
import os


import cv2

#constants

FOCUS_CLOSER = 1
FOCUS_FARTHER = 2


class CameraStation(TotalStation, Camera, StepperMotor):
    '''CameraStation class for TotalStation combinated with camera

        :param name:
        :param measureUnit:
    '''
    #, name, measureUnit, measureIface     , writerUnit = None
    def __init__(self, cameraUnit, stepperMotorUnit, camCalibParams = None, speed = 1, halfSteps = False, affinParams = None, useImageCorrection = False):
        #TotalSatation.__init__(self, name, measureUnit, measureIface, writerUnit) cemmented fr tests
        Camera.__init__(self, cameraUnit, camCalibParams)
        StepperMotor.__init__(self, stepperMotorUnit, speed, halfSteps)


        self._affinParams = affinParams

        self._useImageCorrection = useImageCorrection



        #initialize of focus

        contrast = {'ID': 0 , 'pos': self._position, 'contrast': -1}
        self._contrasts = [contrast]#[ID, motorPosition, contarst value(-1 is special initial value)]


    def getContrast(self, mask = None):
        '''take picture and get contarst

            :returns: contrast of taken picture
        '''
        picName = 'focus_pics/focusPic.png'
        self.takePhoto(picName)
        img = cv2.imread(picName)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean, dev = None, None
        if mask == None:
            size = gray.shape

            mask = np.zeros(gray.shape, dtype='uint8')
            cv2.rectangle(mask, (int(size[0]/2) - 25, int(size[1]/2) - 25), (int(size[0]/2) + 25, int(size[1]/2) + 25), 255, -1)

        mean, dev = cv2.meanStdDev(gray, mean, dev, mask)
        os.remove(picName)
        return dev[0][0]
    def autoFocus(self, direction = FOCUS_FARTHER):
        '''set focus on the middle of picture

            :param direction: start direction
        '''
        while True:
            contrast = {}
            if direction == FOCUS_FARTHER:
                #print(self._contrasts[-1]['contrast'])

                self.turnTo(20)
                contrast['ID'] = self._contrasts[-1]['ID'] + 1
                contrast['pos'] = self._position
                contrast['contrast'] = self.getContrast()

                #print(contrast['contrast'])

                if contrast['contrast'] < self._contrasts[-1]['contrast']:
                    direction = FOCUS_CLOSER
            elif direction == FOCUS_CLOSER:
                #print(self._contrasts[-1]['contrast'])

                self.turnTo(-20)
                contrast['ID'] = self._contrasts[-1]['ID'] + 1
                contrast['pos'] = self._position
                contrast['contrast'] = self.getContrast()

                #print(contrast['contrast'])

                if contrast['contrast'] > self._contrasts[-1]['contrast']:
                    direction = FOCUS_FARTHER

            self._contrasts.append(contrast)
            print(abs(self._contrasts[-2]['contrast'] - self._contrasts[-1]['contrast']))

            if abs(self._contrasts[-2]['contrast'] - self._contrasts[-1]['contrast']) < 0.1:
                print('aaaaaaaaaaaaaa')
                print(abs(contrast['contrast'] - self._contrasts[-1]['contrast']))
                break
