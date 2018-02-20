import sys
sys.path.append('ulyxes/pyapi/')
sys.path.append('../lib')
from totalstation import TotalSatation
from camcalibparams import CamCalibParams
from steppermotor import StepperMotor
from picamera import PiCamera
from serialiface import SerialIface

import cv2



class CameraStation(TotalSatation, Camera, StepperMotor):

    def __init__(self, name, measureUnit, measureIface, cameraUnit, writerUnit = None, camCalibParams = None, affinParams = None, useImageCorrection = False):
        TotalSatation().__init__(self, name, measureUnit, measureIface, writerUnit)
        Camera().__init__(self, cameraUnit, camCalibParams)
        StepperMotor().__init__()

        self.__affinParams = affinParams

        self.__useImageCorrection = useImageCorrection


    def focus(self):
        pass
