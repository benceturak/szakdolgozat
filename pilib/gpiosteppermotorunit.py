import itertools
import time
import RPi.GPIO as GPIO

import os
os.path.append('../lib')
from steppermotorunit import StepperMotorUnit

class GPIOStepperMotorUnit(StepperMotorUnit):
    '''Class for stepper motor unit across RPi GPIO port

        :param GPIOmode: type of GPIO pins ID (GPIO.BOARD|GPIO.BCM)
        :param GPIOpins: ID of pins (tuple)
    '''

    def __init__(self, GPIOmode, GPIOpins):
        '''constructor
        '''
        #set GPIO
        GPIO.setmode(GPIOmode)

        if isinstance(GPIOpins, tuple):
            self.__magnets = [[GPIOpins[0], 0],[GPIOpins[1], 0],[GPIOpins[2], 0],[GPIOpins[3], 0]]
            GPIO.setup(self.__GPIOpins[0], GPIO.OUT)
            GPIO.setup(self.__GPIOpins[1], GPIO.OUT)
            GPIO.setup(self.__GPIOpins[2], GPIO.OUT)
            GPIO.setup(self.__GPIOpins[3], GPIO.OUT)
    def getMagnetStatus(self, magnetNum):
        '''getter method for just one magnet

            :param magnetNum: order number of magnet (int) 0-3
            :returns: status of magnet
        '''
        return self.__magnets[magnetNum][1]
    def setMagnetStatus(self, magnetNum, output):
        '''setter method for magnet status

            :param magnetNum: order number of magnet (int) 0-3
            :param output: status of magnet (int or boolean) 1|0 ot True|False
        '''
        GPIO.output(self.__magnets[megnetNum][0], output)
        self.__GPIOpins[megnetNum][1] = output
    def __del__(self):
        '''destruktor
        '''
        GPIO.cleanup()
