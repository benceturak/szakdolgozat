from calibration.calib import Calib
import picamera as cam

camera = cam.PiCamera()

calibration = Calib(camera, 3)

calibration.run()
