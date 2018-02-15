from calibration.camera import Camera
import cv2
import glob

pics = glob.glob("calib_images/*")

print(pics)
Camera.calibration(pics)
