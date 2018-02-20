import os
import cv2
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
            if isinstance(cameraUnit, picamera.Picamera):
                self.__cameraUnit = cameraUnit
        finally:
            pass

        if isinstance(camCalibParams, (CamCalibParams, None)):#check camera calibration parameters
            self.__camCalibParams = camCalibParams
        else:
            raise TypeError('camCalibParams must be CamCalibParams object or None')
    @property
    def camCalibParams(self):
        '''Getter method for camera calibration parameters

            :returns: camera calibration parameters
        '''
        return self.__camCalibParams
    @camCalibParams.setter
    def camCalibParams(self, camCalParams):
        '''setter method for camera calibration parameters

            :param camCalParms: camera calibration parameters
        '''
        if isinstance(camCalibParams, (CamCalibParams, None)):
            self.__camCalibParams = camCalibParams
        else:
            raise TypeError('camCalibParams must be CamCalibParams object or None')
    def takePhoto(self, name):
        '''taking photo method

            :param name: name of image file
        '''
        try:
            if isinstance(self.__cameraUnit, picamera.Picamera):
                self.__cameraUnit.capture(name)
        finally:
            pass
    def startCameraView(self):
        '''Start Camera View method
        '''
        try:
            if isinstance(self.__cameraUnit, picamera.Picamera):
                self.__cameraUnit.start_preview()
        finally:
            pass
    def stopCameraView(self):
        '''Stop Camera View method
        '''
        try:
            if isinstance(self.__cameraUnit, picamera.Picamera):
                self.__cameraUnit.stop_preview()
        finally:
            pass
