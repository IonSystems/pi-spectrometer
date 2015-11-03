from picamera import PiCamera
from picamera import array

class Camera:
    def __init__(self):
        self.res_x = 640
        self.res_y = 480
        
    def get_image(self):
        #Create an instance of PiCamera
        camera = PiCamera()
        #Configure the capture technique
        capture = array.PiRGBArray(camera)
        #Set the camera resolution
        camera.resolution = (self.res_x, self.res_y)
        #camera.start_preview()
        #time.sleep(3)
        camera.capture(capture, format ="bgr")
        img = capture.array
        
        camera.close()
        return img
