import itertools
import time
import RPi.GPIO as GPIO
import lib.steppermotorunit

class GPIOStepperMotorUnit(lib.steppermotorunit.StepperMotorUnit):
    '''Class for stepper motor unit across RPi GPIO port

        :param GPIOmode: type of GPIO pins ID (GPIO.BOARD|GPIO.BCM)
        :param GPIOpins: ID of pins (tuple)
    '''

    def __init__(self, GPIOmode, GPIOpins):
        '''constructor
        '''
        #set GPIO
        GPIO.setmode(GPIOmode)
        print('b')

        if isinstance(GPIOpins, tuple):
            self.__magnets = [[GPIOpins[0], 1],[GPIOpins[1], 0],[GPIOpins[2], 0],[GPIOpins[3], 0]]
            GPIO.setup(self.__magnets[0], GPIO.OUT)
            GPIO.setup(self.__magnets[1], GPIO.OUT)
            GPIO.setup(self.__magnets[2], GPIO.OUT)
            GPIO.setup(self.__magnets[3], GPIO.OUT)
            GPIO.output(self.__magnets[0][0], 1)
        else:
            raise TypeError('GPIOpins must be tuple!')
    def getMagnetStatus(self, magnetNum):
        '''getter method for just one magnet

            :param magnetNum: order number of magnet (int) 0-3
            :returns: status of magnet (int) 0|1
        '''
        return self.__magnets[magnetNum][1]
    def setMagnetStatus(self, magnetNum, output):
        '''setter method for magnet status

            :param magnetNum: order number of magnet (int) 0-3
            :param output: status of magnet (int or boolean) 1|0 ot True|False
        '''
        GPIO.output(self.__magnets[magnetNum][0], output)
        self.__magnets[magnetNum][1] = output
    def __del__(self):
        '''destruktor
        '''
        GPIO.cleanup()
