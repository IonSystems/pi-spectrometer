import Tkinter
from Tkinter import *
#from Tkinter import Button
from picamera import PiCamera
from picamera import array
import time
import cv2
import Image
import ImageTk

class SpectrometerGUI(Tkinter.Tk):
    def __init__(self):
        
        Tkinter.Tk.__init__(self)
        self.title = "Heriot-Watt University Pi Spectrometer"
        self.wm_title = self.title
        self.label = Tkinter.Label(text="Image", compound="top")
        self.label.pack(side="top", padx=8, pady=8)
        self.iteration=0
        self.UpdateImage(10)

        self.analyseButton = Button(self, text = "Analyse", fg  = "blue", command = self.buttonClicked)
        self.analyseButton.pack(side = BOTTOM)

        #self.bind("<Button-1>", )
        #self.pack()
    def buttonClicked(self):
        self.analyseButton["text"] = "Analysing"
        self.analyseButton["state"] = 'disabled'
        self.doAnalysis()
        self.analyseButton["state"] = "normal"

    def UpdateImage(self, delay, event=None):
        self.iteration += 1

        self.image = self.get_image()
        self.label.configure(image=self.image, text="Iteration %s" % self.iteration)
        self.after(delay, self.UpdateImage, 1000)

    def get_image(self):
        #Create an instance of PiCamera
        camera = PiCamera()
        #Configure the capture technique
        capture = array.PiRGBArray(camera)
        #Set the camera resolution
        camera.resolution = (640, 480)
        #camera.start_preview()
        #time.sleep(3)
        camera.capture(capture, format ="bgr")
        img = capture.array
        b,g,r = cv2.split(img)
        img2 = cv2.merge((r,g,b))
        imgFromArray = Image.fromarray(img2)
        imgtk = ImageTk.PhotoImage(image=imgFromArray)
        #Tkinter.Label(self, image = imgtk).pack()
        camera.close()
        return imgtk

    def doAnalysis(self):
        

if __name__ == "__main__":
    app = SpectrometerGUI()
    app.mainloop()
