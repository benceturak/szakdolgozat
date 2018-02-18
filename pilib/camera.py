import picamera


class Camera(picamera.PiCamera):

    def __init__(self, calibParams = None):
        super().__init__()
        self.__calibParams = calibParams
    @property
    def calibParams(self):
        return self.__calibParams
    @calibParams.setter
    def calibParams(self, params):
        self.__calibParams = calibParams
