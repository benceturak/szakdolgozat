import sys
sys.path.append('lib/')
sys.path.append('ulyxes/pyapi/')
from leicatps1200 import LeicaTPS1200
from remotemeasureunit import RemoteMeasureUnit
from tcpiface import TCPIface
from totalstationclient import TotalStationClient
from camerastation import CameraStation
import logging
from angle import Angle
import cv2
import numpy as np
import io
import time
mu = RemoteMeasureUnit()

iface = TCPIface('test', ('192.168.0.51', 8081), timeout=25)

ts = CameraStation('test', mu, iface)

pic = ts.TakePhoto('stream', 'png')

f = open('h725.png', 'wb')
f.write(pic)
f.close()
print(pic)

print(sys.getsizeof(pic))

#image_stream = io.BytesIO()
#image_stream.write(connection.read(image_len))
#image_st ream.seek(0)
#file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)
#img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

#print(img)
print('----------------- ')
#cv2.namedWindow('check', cv2.WINDOW_NORMAL)
#cv2.imshow('check', img)
#cv2.resizeWindow('check', 600, 600)
#cv2.waitKey()
