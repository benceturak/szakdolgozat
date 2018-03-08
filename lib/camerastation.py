import sys
sys.path.append('ulyxes/pyapi/')
sys.path.append('lib/')
from totalstation import TotalStation
from serialiface import SerialIface
from camera import Camera
from camcalibparams import CamCalibParams
from steppermotor import StepperMotor
from picamera import PiCamera
from imgprocess import ImgProcess
import numpy as np
import os
import cv2


class CameraStation(TotalStation, Camera, StepperMotor):
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
    def __init__(self, name, measureUnit, measureIface, cameraUnit, stepperMotorUnit, writerUnit = None, camCalibParams = None, speed = 1, halfSteps = False, affinParams = np.empty((2,2), int), useImageCorrection = False):
        '''constructor
        '''
        TotalStation.__init__(self, name, measureUnit, measureIface, writerUnit)
        Camera.__init__(self, cameraUnit, camCalibParams)
        StepperMotor.__init__(self, stepperMotorUnit, speed, halfSteps)


        self._affinParams = affinParams

        self._useImageCorrection = useImageCorrection
        #initialize of focus

        self._contrasts = [{'pos': self._position, 'contrast': -1}]


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
            if direction == self.FOCUS_FARTHER:
                #print(self._contrasts[-1]['contrast'])

                self.turnTo(20)
                contrast['pos'] = self._position
                contrast['contrast'] = self.getContrast()

                #print(contrast['contrast'])

                if contrast['contrast'] < self._contrasts[-1]['contrast']:
                    direction = self.FOCUS_CLOSER
            elif direction == self.FOCUS_CLOSER:
                #print(self._contrasts[-1]['contrast'])

                self.turnTo(-20)
                contrast['pos'] = self._position
                contrast['contrast'] = self.getContrast()

                #print(contrast['contrast'])

                if contrast['contrast'] > self._contrasts[-1]['contrast']:
                    direction = self.FOCUS_FARTHER

            self._contrasts.append(contrast)
            #print(abs(self._contrasts[-2]['contrast'] - self._contrasts[-1]['contrast']))

            if abs(self._contrasts[-2]['contrast'] - self._contrasts[-1]['contrast']) < 0.1:
                print(abs(contrast['contrast'] - self._contrasts[-1]['contrast']))
                #break
    def affinCalibration(self):
        '''determine the affin transformation parameters

        '''

        picNum = 0

        picName = 'affin_calib/affin_calib_' + str(self._position) + '_' + str(picNum) + '.png'

        while True:
            print('Target on the marker!')
            self.takePhoto(picName)


            answer = input("Do you want to ")

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
        StepperMotor.__del__(self)
