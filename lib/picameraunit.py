import sys
import cv2
import numpy as np
import os
sys.path.append('../ulyxes/pyapi/')
from measureunit import MeasureUnit
try:
    import picamera
except:
    pass
class PiCameraUnit(MeasureUnit):

    def __init__(self, name = None, typ = None):
        MeasureUnit.__init__(self, name, typ)
        self.cam = picamera.PiCamera()


    def TakePhotoMsg(self, pic, resolution = (720, 480)):
        self.cam.resolution = resolution
        self.cam.capture(pic)
        return {'ret': {}, 'pic': pic}

    def StartCameraViewMsg(self):

        self.cam.start_preview()
        return {'ret': {}}

    def StopCameraViewMsg(self):

        self.cam.stop_preview()
        return {'ret': {}}

    def GetContrastMsg(self, mask):
        picName = 'focus_pics/focusPic.png'
        self.TakePhotoMsg(picName)
        img = cv2.imread(picName)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mean, dev = None, None
        if mask == None:
            size = gray.shape
            mask = np.zeros(gray.shape, dtype='uint8')
            cv2.rectangle(mask, (int(size[0]/2) - 10, int(size[1]/2) - 10), (int(size[0]/2) + 10, int(size[1]/2) + 10), 255, -1)

        mean, dev = cv2.meanStdDev(gray, mean, dev, mask)
        os.remove(picName)
        return {'ret': 0, 'contrast': dev[0][0]}

    def __del__(self):
        self.cam.close()
