from lib.camerastation import CameraStation
from lib.gpiosteppermotorunit import GPIOStepperMotorUnit
from lib.camera import Camera
import picamera
import RPi.GPIO as GPIO

pins = (18, 23, 24, 25)

motorUnit = GPIOStepperMotorUnit(GPIO.BCM, pins)

camera = picamera.PiCamera()

motor = GPIOStepperMotorUnit(GPIO.BCM, pins)

station = CameraStation(camera, motor)

station.autoFocus()

del station
