import os
import cv2
from camcalibparams import CamCalibParams
try:
    import picamera
except:
    pass

class Camera(object):
    ''' Class for handle difference camera unit

        :param cameraUnit: camera unit (PiCamera)
        :param camCalibParams: camera calibration parameters, optional
    '''

    def __init__(self, cameraUnit, camCalibParams = None):
        '''contructor
        '''
        #check camera unit type
        try:
            if isinstance(cameraUnit, picamera.PiCamera):
                self._cameraUnit = cameraUnit
        finally:
            pass#presently only PiCamera is available
        print(camCalibParams)
        if isinstance(camCalibParams, (CamCalibParams)) or camCalibParams == None:#check camera calibration parameters
            self._camCalibParams = camCalibParams
        else:
            raise TypeError('camCalibParams must be CamCalibParams object or None')
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
    def takePhoto(self, name):
        '''taking photo method

            :param name: name of image file
        '''
        try:
            if isinstance(self._cameraUnit, picamera.PiCamera):
                self._cameraUnit.capture(name)
        finally:
            pass#presently only PiCamera is available
    def startCameraView(self):
        '''Start Camera View method
        '''
        try:
            if isinstance(self._cameraUnit, picamera.PiCamera):
                self._cameraUnit.start_preview()
        finally:
            pass#presently only PiCamera is available
    def stopCameraView(self):
        '''Stop Camera View method
        '''
        try:
            if isinstance(self._cameraUnit, picamera.PiCamera):
                self._cameraUnit.stop_preview()
        finally:
            pass#presently only PiCamera is available
