from calibration.calibration import Calibration
import cv2
import glob
import threading
from multiprocessing import  cpu_count

pics = glob.glob("calib_images/*")

print(pics)
cores = cpu_count()
numOfPics = len(pics)

picsPerCore = numOfPics / cores
remainder = numOfPics % cores
threads = []

first = 0

#calib = Calibration(pics)
#
#calib.findChessboardCorners()
#calib.calibrate()
#calib.save('aaa')
#del calib



calib = Calibration.load('aaa')

print(calib)




#for i in range(cores):


#    if i < remainder:
#        print((picsPerCore + 1)*i)
#        print((picsPerCore + 1)*(i+1))
#        #threads.append(Calibration(pics[(picsPerCore + 1)*i:(picsPerCore + 1)*(i+1)]))
#    else:
#        pass



#Camera.calibration(pics)
