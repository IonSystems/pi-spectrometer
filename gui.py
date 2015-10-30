import Tkinter
from Tkinter import *
from Tkinter import Tk
from Tkinter import Button
from picamera import PiCamera
from picamera import array
import time
import cv2
import Image
import ImageTk
import numpy as np

#************** Utility Functions *****************#
    
'''
Return of shape , nrows, ncols,
where n = nrows * ncols = arr.size
'''
def blockshaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1, nrows, ncols))


class SpectrometerGUI(Tkinter.Tk):
    def __init__(self):
        self.res_x = 640 #Width
        self.res_y = 480 #Height
        self.capture_width = self.res_x
        self.capture_height = 2
        
        self.__capture_area = self.calculate_capture_area(return_tuple=False)
         
        
        Tkinter.Tk.__init__(self)
        self.title = "Heriot-Watt University Pi Spectrometer"
        self.wm_title = self.title
        #self.label = Tkinter.Label(text="Image", compound="top")
        #self.label.pack(side="top", padx=8, pady=8)
        self.iteration=0
        #self.UpdateImage(10)

        self.analyseButton = Button(self, text = "Analyse", fg  = "blue", command = self.buttonClicked)
        self.analyseButton.pack(side = BOTTOM)

        self.spectrum = Tkinter.Label(text="Spectrum", compound = "top")
        self.spectrum.pack(side="top", padx=8, pady = 8)

        self.image = self.get_image()

        self.canvas = Tkinter.Canvas(self, width = self.res_x, height = self.res_y, bd=2, bg="white")

        self.canvas.create_image(self.res_x/2, self.res_y/2, image = self.image)
        self.canvas.pack()
        #self.canvas.create_polygon(self.__capture_area, fill="black")
        #self.canvas.create_polygon(0,0,1,1,2,2, 40,40)
        #self.canvas.create_rectangle(50, 25, 150, 75)
        
        x = (self.capture_height)/2
        y = (self.capture_height)/2
        w = self.capture_width
        h = self.capture_height
        self.canvas.create_rectangle(self.res_x/2-self.capture_width/2, self.res_y/2-self.capture_height/2, w, h)
        #self.canvas.create_rectangle(x,y,w,h)
        print "X:%s, Y:%s, W:%s, H:%s",x, y, w, h
        #0,0 is top left
        #left_offset, top_offset, width, height
        #self.canvas.create_rectangle(10,30,630,470,fill="yellow")
      
       

        #self.bind("<Button-1>", )
        #self.pack()


    def buttonClicked(self):
        self.analyseButton["text"] = "Analysing"
        self.analyseButton["state"] = 'disabled'
        self.doAnalysis()
        self.capture_capture_area()
        self.analyseButton["text"] = "Analyse"
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
        camera.resolution = (self.res_x, self.res_y)
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
        return

    def calculate_capture_area(self, return_tuple = True):
        #TODO: Check if we chould be using the bottom left as 0,0
        #Assuming bottom left is 0,0

        #Work out bottom left corner and work from there.
        b_x = (self.res_x - self.capture_height) / 2
        l_y = (self.res_y - self.capture_width) / 2

        t_x = b_x + self.capture_height
        r_y = l_y + self.capture_width
        
        if return_tuple:
            return {'top':t_x, 'bottom':b_x, 'left':l_y, 'right':r_y}
        #TODO return in another format?
        else:
            return [b_x, l_y, t_x, l_y, t_x, r_y, b_x, r_y]

    def capture_capture_area(self):
        camera = PiCamera()
        camera.resolution = (self.res_x, self.res_y)
        capture = array.PiRGBArray(camera)
        camera.capture(capture, format = "bgr")
        img = capture.array
        b,g,r = cv2.split(img)
        img2 = cv2.merge((r,g,b))
        height = len(img2)
        width = len(img2[0])
        #print blockshaped(img, 2, 640)
        
        #The amount of rows to be removed from the top
        remove_top = (self.res_x - self.capture_height)/2
        
        #The amount of rows to be kept, after the above has been removed.
        keep_middle = self.capture_height
        
        trimmedheight = img2[remove_top:] #Remove first x rows
        trimmedheight = trimmedheight[:keep_middle] #Keep first x rows
        print "Height: " + str(len(trimmedheight))
        print "Width: " + str(len(trimmedheight[0]))

        #Flip the array to ve can iterate through each column
        flipped = 

        #trimmedwidth = np.dsplit(trimmedheight, 3)
        #print "Height: " + str(len(trimmedwidth[0]))
        #print "Width: " + str(len(trimmedwidth[0][0]))

        
        
if __name__ == "__main__":
    app = SpectrometerGUI()
    app.mainloop()

