from lib.camcalibparams import CamCalibParams
import glob

images = glob.glob('calib_images/*')

print(images)

params = CamCalibParams().load('bbb')



#params.findChessboardCorners(images)
#params.calibrate()
#params.save('bbb')
