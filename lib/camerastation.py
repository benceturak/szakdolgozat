import sys
sys.path.append('ulyxes/pyapi/')
sys.path.append('lib/')
from totalstation import TotalStation
from serialiface import SerialIface
from camera import Camera
from camcalibparams import CamCalibParams
from steppermotor import StepperMotor
from picamera import PiCamera


import cv2

#constants

FOCUS_CLOSER = 1
FOCUS_FARTHER = 1


class CameraStation(StepperMotor):
    #, name, measureUnit, measureIface     , writerUnit = None
    def __init__(self, cameraUnit, stepperMotorUnit, camCalibParams = None, speed = 1, halfSteps = False, affinParams = None, useImageCorrection = False):
        #TotalSatation().__init__(self, name, measureUnit, measureIface, writerUnit) cemmented fr tests
        #super().__init__(self, cameraUnit, camCalibParams)
        #super().__init__(self, stepperMotorUnit, speed, halfSteps)

        print(self.__position)

        self.__affinParams = affinParams

        self.__useImageCorrection = useImageCorrection



        #initialize of focus

        contrast = {'ID': 0 , 'pos': self.__position, 'contrast': -1}
        self.__contrasts = [contrast]#[ID, motorPosition, contarst value(-1 is special initial value)]


    def getContrast(self, mask = None):
        '''take picture and get contarst

            :returns: contrast of taken picture
        '''

        picName = 'focusPic' + int(self.__contrasts[-1]['ID'] + 1) + '.png'

        self.takePhoto(picName)

        img = cv2.imread(picName)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean, dev = None, None

        if mask == None:
            size = gray.shape

            mask = np.zeros(gray.shape, dtype='uint8')
            cv2.rectangle(mask, (int(size[0]/2) - 25, int(size[1]/2) - 25), (int(size[0]/2) + 25, int(size[1]/2) + 25), 255, -1)

        mean, dev = cv2.meanStdDev(gray, mean, dev, mask)

        return dev


    def autoFocus(self, direction = FOCUS_FARTHER):
        '''set focus on the middle of picture

        '''

        contrast['ID'] = self.__contrasts[-1]['ID'] + 1
        if self.__contrasts[-1]['ID'] == 0:
            contrast['pos']: self.__position
            contrast['contrast']: self.getContrast()



        while True:
            if direction == FOCUS_FARTHER:
                self.turnTo(20)

                curContrast = self.getContrast()

                if curContrast < self.__contrasts[-1]['contrast']:
                    direction = FOCUS_CLOSER

            elif direction == FOCUS_CLOSER:
                self.turnTo(-20)

                curContrast = self.getContrast()

                if curContrast > self.__contrasts[-1]['contrast']:
                    direction = FOCUS_FARTHER
