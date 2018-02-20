import sys
sys.path.append('ulyxes/pyapi/')
sys.path.append('../lib')
from totalstation import TotalSatation
from camcalibparams import CamCalibParams
from steppermotor import StepperMotor
from picamera import PiCamera
from serialiface import SerialIface



class CameraStation(TotalSatation, PiCamera, StepperMotor):

    def __init__(self, name, measureUnit, measureIface, writerUnit = None):
        TotalSatation().__init__(self, name, measureUnit, measureIface, writerUnit)
        PiCamera().__init__()
        StepperMotor().__init__()
