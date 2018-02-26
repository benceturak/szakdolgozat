import itertools
import time
import lib.steppermotorunit
#contants

#turn mode:
STMOTOR_TURN_ABS = 0
STMOTOR_TURN_REL = 1


class StepperMotor(object):
    '''Class for handle difference stepper motor cameraUnit

        :param stepperMotorUnit: stepper motor unit (StepperMotorUnit)
    '''
    def __init__(self, stepperMotorUnit, speed = 1, halfSteps = False):
        '''constructor
        '''
        #set stepperMotorUnit
        if isinstance(stepperMotorUnit, lib.steppermotorunit.StepperMotorUnit):
            self.__stepperMotorUnit = stepperMotorUnit
        else:
            raise TypeError()
        #set default position
        self.__position = 0
        if isinstance(halfSteps, bool):
            self.__halfSteps = halfSteps
        else:
            raise TypeError()
        if isinstance(speed, (int, float)) and speed >= 1:
            self.__speed = speed * 0.003
        else:
            raise TypeError()
        #initialize of motor
        self.turnTo(10)
        self.turnTo(-10)
        self.__position = 0
        print('A')
    @property
    def position(self):
        '''getter method for position

            :returns: motor position (int)
        '''
        return self.__position
    @position.setter
    def position(self, pos):
        '''setter method for position (It does not move the motor!)

            :param pos: motor position (int)
        '''
        if isinstance(pos, int):
            self.__position = pos
        else:
            raise TypeError('Position must be integer!')
    @property
    def speed(self):
        '''getter method for motor speed

            :returns: motor speed (int)
        '''
        return int(self.__speed / 0.003)
    @speed.setter
    def speed(self, speed):
        '''setter method for motor speed

            :param speed: motor speed (int)
        '''
        if isinstance(speed, (int, float)) and speed >= 1:
            self.__speed = speed * 0.003
        else:
            raise TypeError('Speed must be integer and greater than 0')
    @property
    def halfSteps(self):
        '''getter method for permit half steps

            :returns: permission of half steps (boolean)
        '''
        return self.__halfSteps
    @halfSteps.setter
    def halfSteps(self, halfSteps):
        '''setter method for permit half steps

            :param halfSteps: premission of half steps (boolean)
        '''
        if isinstance(halfSteps, bool):
            self.__halfSteps = halfSteps
        else:
            raise TypeError('HalfSteps must be boolean!')
    def turnTo(self, pos, posMode = STMOTOR_TURN_REL):
        '''move stepper motor method

            :param pos: turn to this position
            :param posMode: position can be absolute or relative (STMOTOR_TURN_REL|STMOTOR_TURN_ABS)
            :returns: motor position after motor stopped (int)
        '''
        if not isinstance(pos, int):
            raise TypeError('Pos must be integer!')
        if posMode == STMOTOR_TURN_REL:
            for _ in  range(abs(pos)):
                if pos > 0:
                    self.stepForward()
                elif pos < 0:
                    self.stepBackward()
        elif posMode == STMOTOR_TURN_ABS:
            self.turn2(pos - self.__position)
        else:
            raise TypeError('PosMode must be STMOTOR_TURN_REL or STMOTOR_TURN_ABS!')
        return self.__position
    def stepForward(self):
        '''only one step forward method
        '''
        time.sleep(self.__speed)
        if self.__halfSteps:
            for m in range(0, 4):
                if self.__stepperMotorUnit.getMagnetStatus(m) == 1:
                    if m == 0 and self.__stepperMotorUnit.getMagnetStatus(3) == 1:
                        self.__stepperMotorUnit.setMagnetStatus(3, 0)
                    elif m == 3:
                        self.__stepperMotorUnit.setMagnetStatus(0, 1)
                    else:
                        if self.__stepperMotorUnit.getMagnetStatus(m + 1) == 1:
                            self.__stepperMotorUnit.setMagnetStatus(m, 0)
                        else:
                            self.__stepperMotorUnit.setMagnetStatus(m + 1, 1)
                    break
        else:
            for m in range(0, 4):
                if self.__stepperMotorUnit.getMagnetStatus(m) == 1:
                    self.__stepperMotorUnit.setMagnetStatus(m, 0)
                    if m == 3:
                        self.__stepperMotorUnit.setMagnetStatus(0, 1)
                    else:
                        self.__stepperMotorUnit.setMagnetStatus(m + 1, 1)
                    break
        self.__position += 1
    def stepBackward(self):
        '''only one step backward method
        '''
        time.sleep(self.__speed)
        if self.__halfSteps:
            for m in range(0, 4):
                if self.__stepperMotorUnit.getMagnetStatus(m) == 1:
                    if m == 0 and self.__stepperMotorUnit.getMagnetStatus(3) == 1:
                        self.__stepperMotorUnit.setMagnetStatus(0, 0)
                    elif m == 3:
                        self.__stepperMotorUnit.setMagnetStatus(m - 1, 1)
                    else:
                        if self.__stepperMotorUnit.getMagnetStatus(m + 1) == 1:
                            self.__stepperMotorUnit.setMagnetStatus(m + 1, 0)
                        else:
                            self.__stepperMotorUnit.setMagnetStatus(m - 1, 1)
                    break
        else:
            for m in range(0, 4):
                if self.__stepperMotorUnit.getMagnetStatus(m) == 1:
                    self.__stepperMotorUnit.setMagnetStatus(m, 0)
                    if m == 0:
                        self.__stepperMotorUnit.setMagnetStatus(3, 1)
                    else:
                        self.__stepperMotorUnit.setMagnetStatus(m - 1, 1)
                    break
        self.__position -= 1

    def __del__(self):
        '''destructor
        '''
        del self.__stepperMotorUnit
