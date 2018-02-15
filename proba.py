
import picamera as cam

camera = cam.PiCamera()


camera.start_preview()
i = 1
new_pic = True
while new_pic:
    input("press enter")
    camera.capture("calib_images/calib_" + str(i) + ".png")
    i += 1
    answer = input("New picture?(Y|N)")
    if answer == "Y" or answer == "y":
        new_pic = True
    elif answer == "N" or answer == "n":
        new_pic = False
