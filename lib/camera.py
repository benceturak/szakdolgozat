import sys
sys.path.append('../ulyxes/pyapi/')
import os
import cv2
from instrument import Instrument
from camcalibparams import CamCalibParams
from tcpiface import TCPIface

try:
    import picamera
except:
    pass

class Camera(Instrument):
    ''' Class for handle difference camera unit

        :param cameraUnit: camera unit (PiCamera)
        :param camCalibParams: camera calibration parameters, optional
    '''

    def __init__(self, name, measureUnit, measureIface = None, writerUnit = None):
        '''contructor
        '''
        super(Camera, self).__init__(name, measureUnit, measureIface, writerUnit)

        self.measureUnit = measureUnit
    @property
    def camCalibParams(self):
        '''Getter method for camera calibration parameters

            :returns: camera calibration parameters
        '''
        return self._camCalibParams
    @camCalibParams.setter
    def camCalibParams(self, camCalParams):
        '''setter method for camera calibration parameters

            :param camCalParms: camera calibration parameters
        '''
        if isinstance(camCalibParams, (CamCalibParams, None)):
            self._camCalibParams = camCalibParams
        else:
            raise TypeError('camCalibParams must be CamCalibParams object or None')
    def TakePhoto(self, pic, resolution = (480,720)):
        '''taking photo method

            :param name: name of image file
        '''
        msg = self.measureUnit.TakePhotoMsg(pic, resolution)
        if isinstance(msg, str):
            return self._process(msg, pic)
        else:
            return msg
    def StartCameraView(self):
        '''Start Camera View method
        '''
        msg = self.measureUnit.StartCameraViewMsg()

        if msg['ret'] != 0:
            return self._process(msg)
        else:
            return msg['ret']

    def StopCameraView(self):
        '''Stop Camera View method
        '''

        msg = self.measureUnit.StopCameraViewMsg()

        if msg['ret'] != 0:
            return self._process(msg)
        else:
            return msg['ret']

    def GetContrast(self, mask = None):
        '''take picture and get contarst

            :returns: contrast of taken picture
        '''

        msg = self.measureUnit.GetContrastMsg(mask)

        if msg['ret'] != 0:
            return self._process(msg)
        else:
            return msg['contrast']
