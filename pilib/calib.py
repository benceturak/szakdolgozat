
import picamera
import cv2
import os

class Calib(object):
    '''
    Calibration class for picamera
    '''
    def __init__(self, camera, numberOfPhotos = 1, directory = 'calib_images', parallaxisScrew = None):

        if isinstance(camera, picamera.PiCamera):
            self.__camera = camera
        else:
            raise TypeError()

        if isinstance(directory, str):
            if directory != "":
                self.__directory = directory + '/'
            else:
                self.__directory = directory
        else:
            raise TypeError()

        if isinstance(numberOfPhotos, int):
            self.__numberOfPhotos = numberOfPhotos
        else:
            raise TypeError()
        if isinstance(parallaxisScrew, bool):
            self.__parallxisScrew = parallaxisScrew
        else:
            self.__parallxisScrew = parallaxisScrew#temporary
            #raise TypeError()

    @property
    def directory(self):
        return self.__directory

    @directory.setter
    def directory(self, directory):
        if isinstance(directory, str):
            if directory != "":
                self.__directory = directory + '/'
            else:
                self.__directory = directory
        else:
            raise TypeError()


    #def capture(self, fileName):
    #    self.__camera.capture(self.__dir + fileName)

    def takePhotos(self):


        focusNumber = 1
        newFocus = True
        while newFocus:


            self.__camera.start_preview(fullscreen = False, window = (100, 20, 640, 480))#open camera view

            #in case of parallaxis change possibility

            #print("This is the " + i ". focus position.\n")
            #print("Set the focus position")
            #...

            for i in range(0, self.__numberOfPhotos):

                photoPath = str(self.__directory) + "calib_" + str(focusNumber) + "_" + str(i) + ".png"#photo path

                #take new photo and check it
                responseOK = False
                while not responseOK:
                    input("Press enter to take a photo!")#waiting for the user
                    print("New celibration photo: " + photoPath)#response for the user
                    self.__camera.capture(photoPath)#take a photo


                    calibPhoto = cv2.imread(photoPath)
                    cv2.namedWindow(photoPath)
                    cv2.imshow(photoPath, calibPhoto)
                    cv2.waitKey(0)

                    response = input("It's ok?(Y/N)")
                    cv2.destroyAllWindows()
                    if response == "Y" or response == "y" or response == "yes" or response == "Yes":
                        responseOK = True
                    elif response == "N" or response == "n" or response == "no" or response == "no":
                        os.remove(photoPath)#remove photo
                        print("This photo was deleted: " + photoPath)#response for the user
                    else:
                        print("You have to choose yes(Yself.__camera.start_preview(fullscreen = False, window = (100, 20, 640, 480))#open camera view) or no(N)")#invalid answer

            self.__camera.stop_preview()#open camera view
            print("This focus calibration is ended.")
            #ask new calibration loop
            responseOK = False
            while not responseOK:
                response = input("Do you want to take photos in other focus?(Y/N)")
                if response == "Y" or response == "y" or response == "yes" or response == "Yes":
                    focusNumber += 1
                    responseOK = True

                elif response == "N" or response == "n" or response == "no" or response == "no":
                    print("This is the end of taking photos")
                    responseOK = True
                    newFocus = False
                else:
                    print("You have to choose yes(Y) or no(N)")

    def run(self):
        pass
