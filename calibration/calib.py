
import picamera
import cv2

class Calib(object):
    '''
    Calibration class for picamera
    '''
    def __init__(self, camera, directory = 'calib_images', numberOfPhotos = 1, parallaxisScrew = None):

        self.__camera = camera

        if directory != "":
            self.directory = directory + '/'
        else:
            self.directory = directory

        self.__numberOfPhotos = numberOfPhotos
        self.__parallxisScrew = parallaxisScrew

    @directory.setter
    def directory(self, directory):
        self.__directory = directory
    @property
    def directory(self):
        return self.__directory

    #def capture(self, fileName):
    #    self.__camera.capture(self.__dir + fileName)

    def run(self):
        self.__camera.start_preview()#open camera view

        focusNumber = 1
        newFocus = True
        while newFocus:

            #in case of parallaxis change possibility

            #print("This is the " + i ". focus position.\n")
            #print("Set the focus position")
            #...

            for i in range(1, self.__numberOfPhotos):

                photoPath = self.__directory + "calib_" + focusNumber + "_" + i + ".png"#photo path

                #take new photo and check it

                responseOK = False
                while not responseOK:
                    input("Press enter to take a photo!")#waiting for the user
                    self.__camera.capture(photoPath)#take a photo
                    print("New celibration photo: " + photoPath)#response for the user

                    calibPhoto = cv2.imread(photoPath)
                    cv2.namedWindow(photoPath)
                    cv2.imshow(photoPath, calibPhoto)

                    response = input("It's ok?(Y/N)")
                    if response == "Y" or response == "y" or response == "yes" or response == "Yes":
                        responseOK = True
                    elif response == "N" or response == "n" or response == "no" or response == "no":
                        os.remove(photoPath)#remove photo
                        print("This photo was deleted: " + photoPath)#response for the user
                    else:
                        print("You have to choose yes(Y) or no(N)")#invalid answer

            print("This focus calibration is ended.")
            #ask new calibration loop
            responseOK = False
            while not responseOK:
                response = input("Do you want to calibrate in new focus?(Y/N)")
                if response == "Y" or response == "y" or response == "yes" or response == "Yes":
                    focusNumber += 1
                    responseOK = True

                elif response == "N" or response == "n" or response == "no" or response == "no":
                    print("This is the end ")
                    responseOK = True
                    newFocus = False
                else:
                    print("You have to choose yes(Y) or no(N)")
