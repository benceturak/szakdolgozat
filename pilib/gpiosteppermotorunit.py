import itertools
import time
import RPi.GPIO as GPIO

import os
os.path.append('../lib')
from steppermotorunit import StepperMotorUnit

class GPIOStepperMotorUnit(StepperMotorUnit):
    '''Class for stepper motor unit across RPi GPIO port

        :param GPIOmode: type of GPIO pins number, (GPIO.BOARD|GPIO.BCM)
        :param GPIOpins: number of pins (tuple)
    '''

    def __init__(self, GPIOmode, GPIOpins):
        '''constructor
        '''
        #set GPIO
        GPIO.setmode(GPIOmode)

        if isinstance(GPIOpins, tuple):
            self.__GPIOpins = [[GPIOpins[0], 1],[GPIOpins[1], 0],[GPIOpins[2], 0],[GPIOpins[3], 0]]
            GPIO.setup(self.__GPIOpins[0], GPIO.OUT)
            GPIO.setup(self.__GPIOpins[1], GPIO.OUT)
            GPIO.setup(self.__GPIOpins[2], GPIO.OUT)
            GPIO.setup(self.__GPIOpins[3], GPIO.OUT)
    @property
    def GPIOpins(self):
        '''getter method for GPIO pins

            :returns: GPIO pins number as setted up GPIO mode and pins values
        '''
        return self.__GPIOpins
    def getGPIOpin(self, pin):
        '''getter method for just one GPIO pins

            :param pin: order number of pin (int) 0-3
            :returns: value of pin
        '''
        return self.__GPIOpins[pin][1]
    def setGPIOpin(self, pin, output):
        '''set GPIO pins output method

            :param pin: order number of pin (int) 0-3
            :param outpur: value of pin (int or boolean) 1|0 ot True|False
        '''
        GPIO.output(self.__GPIOpins[pin][0], output)
        self.__GPIOpins[pin][1] = output
    def __del__(self):
        '''destruktor
        '''
        GPIO.cleanup()
