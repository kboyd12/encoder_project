import time
import picamera
import numpy as np
import tkinter
print("BC is a stud")
# Create an array representing a 1280x720 image of
# a cross through the center of the display. The shape of
# the array must be of the form (height, width, color)

root = tkinter.Tk()
width = root.winfo_screenwidth()
height = root.winfo_screenheight()


with picamera.PiCamera() as camera:
    camera.resolution = (1280, 720)
    camera.framerate = 30
    camera.sensor_mode = 6

    a = np.zeros((720, 1280, 3), dtype=np.uint8)
    a[360, :, :] = 0xff
    a[:, 640, :] = 0xff

    camera.start_preview()
    camera.preview.fullscreen = False
    camera.preview.window = (0, 0, width, int(height/1.5))
    # Add the overlay directly into layer 3 with transparency;
    # we can omit the size parameter of add_overlay as the
    # size is the same as the camera's resolution
    o = camera.add_overlay(a.tobytes(), layer=3, alpha=64)
    try:
        # Wait indefinitely until the user terminates the script
        while True:
            time.sleep(1)
    finally:
        camera.remove_overlay(o)
