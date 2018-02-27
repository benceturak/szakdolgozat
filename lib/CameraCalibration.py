import cv2
import numpy as np
import threading
from multiprocessing import  cpu_count
import pickle


class CameraCalibration(object):
    '''
    Camera calibration
    '''
    def __init__(self, pics, patternSize = (9,6)):
        self._pics = pics
        self._patternSize = patternSize
        self._objpoints = []
        self._imgpoints = []
        self._errPics = []
        self._goodPics = 0


    def findChessboardCorners(self):

        objp = np.zeros((self._patternSize[0] * self._patternSize[1],3), np.float32)
        objp[:,:2] = np.mgrid[0:self._patternSize[0],0:self._patternSize[1]].T.reshape(-1,2)

        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)



        for pic in self._pics:
            print('Corners searcing on: ' + pic)
            img = cv2.imread(pic)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(gray, self._patternSize)

            if ret == True:
                print("Corners are found")
                self._objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
                self._imgpoints.append(corners2)
                self._goodPics += 1
            else:
                print("Corners are not found!")
                self._errPics.append(pic)
        print(str(self._goodPics) + "pictures are good")

    def save(self, path = ''):
        with open(path, "wb") as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(path):
        with open(path, "rb") as f:
            return pickle.load(f)

    def calibrate(self):
        img = cv2.imread(self._pics[0])
        print(img.shape[::-1][1:3])

        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(self._objpoints, self._imgpoints, img.shape[::-1][1:3], None, None)

        print(ret)
        print(mtx)
        print(dist)
        print(rvecs)
        print(tvecs)
