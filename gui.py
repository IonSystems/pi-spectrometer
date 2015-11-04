import Tkinter
from Tkinter import *
from Tkinter import Tk
from Tkinter import Button
import time
import gc
import cv2
import Image
import ImageTk
import sys
import matplotlib
matplotlib.use('SVG')
from matplotlib import pyplot
import pylab
pylab.ion() #Turn on interactive graph
from PIL import Image
import webbrowser
from matplotlib.ticker import MultipleLocator, FormatStrFormatter

import utils
from spectrometer import Spectrometer

class SpectrometerGUI(Tkinter.Tk):
    def __init__(self, spectrometer):
        self.rectangle = 0        
        self.spectrometer = spectrometer
       
        #Define properties of graph
        self.x_min_range = 430
        self.x_max_range = 650
        self.box_width = self.spectrometer.camera.res_x
        self.box_height = 2
        self.box_x = 0
        self.box_y = self.spectrometer.camera.res_y/2 - self.box_height/2
        
        
         
        
        Tkinter.Tk.__init__(self)
        
        Tkinter.Tk.wm_title(self, "Heriot-Watt University Pi Spectrometer")
        
        logo = Tkinter.PhotoImage(file = "img/logo/favicon32.png")
        self.tk.call('wm', 'iconphoto', self._w, logo)
    
        self.iteration=0
        #self.UpdateImage(10)   
        self.canvas = Canvas(self, width = self.spectrometer.camera.res_x, height = self.spectrometer.camera.res_y, bd=2, bg="white")

        self.analyseButton = Button(self, text = "Analyse", fg  = "blue", command = self.buttonClicked)
        self.analyseButton.pack(side = BOTTOM)
        self.widthPlusButton = Button(self, text = "Width +", fg  = "black", command = self.changeWidth(1, self.canvas))
        self.widthPlusButton.pack(side = BOTTOM)
        self.widthMinusButton = Button(self, text = "Width -", fg  = "red", command = self.changeWidth(-1, self.canvas))
        self.widthMinusButton.pack(side = BOTTOM)
        self.heightPlusButton = Button(self, text = "Height +", fg  = "black", command = self.changeHeight(1, self.canvas))
        self.heightPlusButton.pack(side = BOTTOM)
        self.heightMinusButton = Button(self, text = "Height -", fg  = "red", command = self.changeHeight(-1, self.canvas))
        self.heightMinusButton.pack(side = BOTTOM)
        self.xPositionPlusButton = Button(self, text = "X_Position +", fg  = "black", command = self.changeXPosition(1, self.canvas))
        self.xPositionPlusButton.pack(side = BOTTOM)
        self.xPositionMinusButton = Button(self, text = "X_Postition -", fg  = "red", command = self.changeXPosition(-1, self.canvas))
        self.xPositionMinusButton.pack(side = BOTTOM)
        self.yPositionPlusButton = Button(self, text = "Y_Postition +", fg  = "black", command = self.changeYPosition(1, self.canvas))
        self.yPositionPlusButton.pack(side = BOTTOM)
        self.yPositionMinusButton = Button(self, text = "Y_Position -", fg  = "red", command = self.changeYPosition(-1, self.canvas))
        self.yPositionMinusButton.pack(side = BOTTOM)
        self.spectrum = Tkinter.Label(text="Spectrum", compound = "top")
        self.spectrum.pack(side="top", padx=8, pady = 8)

        self.image = self.spectrometer.camera.get_image()
        b,g,r = cv2.split(self.image)
        img2 = cv2.merge((r,g,b))
        imgFromArray = Image.fromarray(img2)
        self.tk_image = ImageTk.PhotoImage(image=imgFromArray)
        

        
        self.image_on_canvas = self.canvas.create_image(self.spectrometer.camera.res_x/2, self.spectrometer.camera.res_y/2, image = self.tk_image)
       
        
        
        self.rectangle = self.canvas.create_rectangle(self.box_x, self.box_y, self.box_x + self.box_width, self.box_y + self.box_height)
        self.canvas.pack()
       
        self.UpdateImage(0)
    
        

    def draw_line_graph(self, wavelengths, intensities):

        #Sort the lists
        wavelengths, intensities = (list(t) for t in zip(*sorted(zip(wavelengths, intensities))))

        Max = max(intensities) * 1.0
        intensities[:] = [x / Max for x in intensities]
        #for intensity in intensities:
        #    intensity /= max(intensities)        

        majorLocator = MultipleLocator(20)
        majorFormatter = FormatStrFormatter('%d')
        minorLocator = MultipleLocator(5)        
        
        pyplot.axis([self.x_min_range,self.x_max_range,0,max(intensities)])

        fig, ax = pyplot.subplots()
        #pyplot.plot(wavelengths,intensities)
        #pyplot.hist(wavelengths)
        pyplot.bar(wavelengths, intensities, width=1)
        ax.xaxis.set_major_locator(majorLocator)
        ax.xaxis.set_major_formatter(majorFormatter)
        ax.xaxis.set_minor_locator(minorLocator)
        pyplot.xlabel("Wavelength")
        pyplot.ylabel("Intensity")
        
        #pyplot.show()
        pyplot.savefig('/home/pi/spectrometer/graph.png')
        webbrowser.open('/home/pi/spectrometer/graph.png')

    
    def buttonClicked(self):
        self.analyseButton["text"] = "Analysing"
        self.analyseButton["state"] = 'disabled'
        calded = self.spectrometer.capture_capture_area(self.image)
        self.draw_line_graph(calded[0], calded[1])
        self.analyseButton["text"] = "Analyse"
        self.analyseButton["state"] = "normal"

        
    def changeWidth(self, pixels, canvas):
        self.box_width += pixels
        #del self.rectangle
        self.canvas.delete(self.rectangle)
        self.rectangle = canvas.create_rectangle(self.box_x, self.box_y, self.box_x + self.box_width, self.box_y + self.box_height)
        #self.canvas.itemconfig(self.image_on_canvas, image = self.tk_image)
    def changeHeight(self, pixels, canvas):
        self.box_height += pixels
        #del self.rectangle
        self.canvas.delete(self.rectangle)
        self.rectangle = canvas.create_rectangle(self.box_x, self.box_y, self.box_x + self.box_width, self.box_y + self.box_height)
        
    def changeXPosition(self, pixels, canvas):
        self.box_x += 5*pixels
        #del self.rectangle
        self.canvas.delete(self.rectangle)
        self.rectangle = canvas.create_rectangle(self.box_x, self.box_y, self.box_x + self.box_width, self.box_y + self.box_height)
        
    def changeYPosition(self, pixels, canvas):
        self.box_y += 5*pixels
        #del self.rectangle
        self.canvas.delete(self.rectangle)
        self.rectangle = canvas.create_rectangle(self.box_x, self.box_y, self.box_x + self.box_width, self.box_y + self.box_height)
        
    def UpdateImage(self, delay, event=None):
        self.iteration += 1

        self.image = self.spectrometer.camera.get_image()
        b,g,r = cv2.split(self.image)
        img2 = cv2.merge((r,g,b))
        imgFromArray = Image.fromarray(img2)
        self.tk_image = ImageTk.PhotoImage(image=imgFromArray)
        #self.canvas.create_image(self.spectrometer.camera.res_x/2, self.spectrometer.camera.res_y/2, image = imgtk)
        
        self.canvas.itemconfig(self.image_on_canvas, image = self.tk_image)
        self.after(delay, self.UpdateImage, 2000)

        
if __name__ == "__main__":
    spectrometer = Spectrometer()
    app = SpectrometerGUI(spectrometer)
    app.mainloop()

