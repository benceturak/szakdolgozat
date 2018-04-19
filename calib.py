import sys
sys.path.append('lib/')
from cameracalibration import CameraCalibration


pics = ('pic_0.png','pic_1.png','pic_2.png','pic_3.png',)

calib = CameraCalibration(pics, (3,3))

calib.findChessboardCorners()
