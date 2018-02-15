import itertools
import time
import RPi.GPIO as GPIO

#contants

#turn mode:
STMOTOR_TURN_ABS = 0
STMOTOR_TURN_REL = 1



class StMotor(object):

    def __init__(self, GPIOmode, GPIOpins, speed = 1, halfSteps = False):
        #set default position
        self.__position = 0
        if isinstance(halfSteps, bool):
            self.__halfSteps = halfSteps
        else:
            raise TypeError()
        if isinstance(speed, int):
            self.__speed = speed * 0.003
        else:
            raise TypeError()
        #set GPIO
        GPIO.setmode(GPIOmode)

        self.__GPIOpins = [[GPIOpins[0], 1],[GPIOpins[1], 0],[GPIOpins[2], 0],[GPIOpins[3], 0]]
        GPIO.setup(self.__GPIOpins[0], GPIO.OUT)
        GPIO.setup(self.__GPIOpins[1], GPIO.OUT)
        GPIO.setup(self.__GPIOpins[2], GPIO.OUT)
        GPIO.setup(self.__GPIOpins[3], GPIO.OUT)

        GPIO.output(self.__GPIOpins[0][0], 1)
        self.turn2(10)
        self.__position = 0
    @property
    def position(self):
        return self.__position
    @property
    def halfSteps(self):
        return self.__halfSteps
    @halfSteps.setter
    def halfSteps(self, halfSteps):
        if isinstance(halfSteps, bool):
            self.__halfSteps = halfSteps
        else:
            raise TypeError()
    @property
    def GPIOpins(self):
        return self.__GPIOpins
    def turn2(self, pos, turnMode = STMOTOR_TURN_REL):
        if not isinstance(pos, int):
            raise TypeError
        if turnMode == STMOTOR_TURN_REL:
            for _ in  range(abs(pos)):
                if pos > 0:
                    self.stepForward()
                elif pos < 0:
                    self.stepBackward()
                print(self.__position)

        elif turnMode == STMOTOR_TURN_ABS:
            self.turn2(pos - self.__position)
        else:
            raise TypeError
    def stepForward(self):
        time.sleep(self.__speed)
        if self.__halfSteps:
            for pin in range(0, 4):
                if self.__GPIOpins[pin][1] == 1:
                    if pin == 0 and self.__GPIOpins[3][1] == 1:
                        GPIO.output(self.__GPIOpins[3][0], 0)
                        self.__GPIOpins[3][1] = 0
                    elif pin == 3:
                        GPIO.output(self.__GPIOpins[0][0], 1)
                        self.__GPIOpins[0][1] = 1
                    else:
                        if self.__GPIOpins[pin + 1][1] == 1:
                            GPIO.output(self.__GPIOpins[pin][0], 0)
                            self.__GPIOpins[pin][1] = 0
                        else:
                            GPIO.output(self.__GPIOpins[pin + 1][0], 1)
                            self.__GPIOpins[pin + 1][1] = 1
                    break
        else:
            for pin in range(0, 4):
                if self.__GPIOpins[pin][1] == 1:
                    GPIO.output(self.__GPIOpins[pin][0], 0)
                    self.__GPIOpins[pin][1] = 0
                    if pin == 3:
                        GPIO.output(self.__GPIOpins[0][0], 1)
                        self.__GPIOpins[0][1] = 1
                    else:
                        GPIO.output(self.__GPIOpins[pin + 1][0], 1)
                        self.__GPIOpins[pin + 1][1] = 1
                    break
        self.__position += 1
    def stepBackward(self):
        time.sleep(self.__speed)
        if self.__halfSteps:
            for pin in range(0, 4):
                if self.__GPIOpins[pin][1] == 1:
                    if pin == 0 and self.__GPIOpins[3][1] == 1:
                        GPIO.output(self.__GPIOpins[0][0], 0)
                        self.__GPIOpins[0][1] = 0
                    elif pin == 3:
                        GPIO.output(self.__GPIOpins[pin - 1][0], 1)
                        self.__GPIOpins[pin - 1][1] = 1
                    else:
                        if self.__GPIOpins[pin + 1][1] == 1:
                            GPIO.output(self.__GPIOpins[pin + 1][0], 0)
                            self.__GPIOpins[pin + 1][1] = 0
                        else:
                            GPIO.output(self.__GPIOpins[pin - 1][0], 1)
                            self.__GPIOpins[pin - 1][1] = 1
                    break
        else:
            for pin in range(0, 4):
                if self.__GPIOpins[pin][1] == 1:
                    GPIO.output(self.__GPIOpins[pin][0], 0)
                    self.__GPIOpins[pin][1] = 0
                    if pin == 0:
                        GPIO.output(self.__GPIOpins[3][0], 1)
                        self.__GPIOpins[3][1] = 1
                    else:
                        GPIO.output(self.__GPIOpins[pin - 1][0], 1)
                        self.__GPIOpins[pin - 1][1] = 1
                    break
        self.__position -= 1

    def __del__(self):
        GPIO.cleanup()
