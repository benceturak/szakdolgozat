import picamera
import cv2
import numpy as np

class Camera(picamera.PiCamera):

    def __init__(self, calibParams = None):
        super().__init__()
        self.__calibParams = calibParams
    @property
    def calibParams(self):
        return self.__calibParams
    @calibParams.setter
    def calibParams(self, params):
        self.__calibParams = calibParams

    @staticmethod
    def calibration(pics, patternSize = (7,6)):

        objp = np.zeros((patternSize[0] * patternSize[1],3), np.float32)
        objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        objpoints = []
        imgpoints = []

        for pic in pics:
            print(pic)
            img = cv2.imread(pic)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(gray, patternSize)

            if ret == True:
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                imgpoints.append(corners2)
