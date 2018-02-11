import GPIO
class StMotor(object):

    def __init__(self, GPIOmode, GPIOpins, halfSteps = False):

        #set GPIO
        GPIO.setmode(GPIOmode)

        self.__GPIOpins = [[GPIOpins[0], 0],[GPIOpins[1], 0],[GPIOpins[2], 0],[GPIOpins[3], 0]]


        GPIO.setup(self.__GPIOpins[0], GPIO.OUT)
        GPIO.setup(self.__GPIOpins[1], GPIO.OUT)
        GPIO.setup(self.__GPIOpins[2], GPIO.OUT)
        GPIO.setup(self.__GPIOpins[3], GPIO.OUT)

        self.halfSteps = halfSteps

    @halfSteps.setter
    def halpSteps(self, halpSteps):
        if isinstance(halfSteps, bool):
            self.__halfSteps = halfSteps
        else:
            raise TypeError()

    def stepForward(self):
        if self.__halfSteps:
            for pin in range(0, 4):
                if self.__GPIOpins[pin][1] == 1:
                    if pin == 3:
                        if self.__GPIOpins[0][1] == 1:
                            GPIO.output(self.__GPIOpins[pin][0], 0)
                            self.__GPIOpins[pin][1] = 0
                        else:
                            GPIO.output(self.__GPIOpins[0][0], 1)
                            self.__GPIOpins[0][1] = 1
                    else:
                        if self.__GPIOpins[pin + 1][1] == 1:
                            GPIO.output(self.__GPIOpins[pin][0], 0)
                            self.__GPIOpins[pin][1] = 0
                        else:
                            GPIO.output(self.__GPIOpins[pin + 1][0], 0)
                            self.__GPIOpins[pin + 1][1] = 0
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





    def stepBackward(self):
        if self.__halfSteps:
            for pin in range(0, 4):
                if self.__GPIOpins[pin][1] == 1:
                    if pin == 0:
                        if self.__GPIOpins[3][1] == 1:
                            GPIO.output(self.__GPIOpins[pin][0], 0)
                            self.__GPIOpins[pin][1] = 0
                        else:
                            GPIO.output(self.__GPIOpins[3][0], 1)
                            self.__GPIOpins[3][1] = 1
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
                    if pin == 3:
                        GPIO.output(self.__GPIOpins[0][0], 1)
                        self.__GPIOpins[0][1] = 1
                    else:
                        GPIO.output(self.__GPIOpins[pin + 1][0], 1)
                        self.__GPIOpins[pin + 1][1] = 1
                    break
