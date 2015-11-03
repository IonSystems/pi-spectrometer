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
        
        self.spectrometer = spectrometer
       
        #Define properties of graph
        self.x_min_range = 430
        self.x_max_range = 650
        
        #self.__capture_area = self.calculate_capture_area(return_tuple=False)
         
        
        Tkinter.Tk.__init__(self)
        
        Tkinter.Tk.wm_title(self, "Heriot-Watt University Pi Spectrometer")
        
        logo = Tkinter.PhotoImage(file = "img/logo/favicon32.png")
        self.tk.call('wm', 'iconphoto', self._w, logo)
    
        self.iteration=0
        #self.UpdateImage(10)

        self.analyseButton = Button(self, text = "Analyse", fg  = "blue", command = self.buttonClicked)
        self.analyseButton.pack(side = BOTTOM)

        self.spectrum = Tkinter.Label(text="Spectrum", compound = "top")
        self.spectrum.pack(side="top", padx=8, pady = 8)

        self.image = self.spectrometer.camera.get_image()
        b,g,r = cv2.split(self.image)
        img2 = cv2.merge((r,g,b))
        imgFromArray = Image.fromarray(img2)
        self.tk_image = ImageTk.PhotoImage(image=imgFromArray)
        #Tkinter.Label(self, image = imgtk).pack()

        self.canvas = Tkinter.Canvas(self, width = self.spectrometer.camera.res_x, height = self.spectrometer.camera.res_y, bd=2, bg="white")

        self.image_on_canvas = self.canvas.create_image(self.spectrometer.camera.res_x/2, self.spectrometer.camera.res_y/2, image = self.tk_image)
        self.canvas.pack()
        #self.canvas.create_polygon(self.__capture_area, fill="black")
        #self.canvas.create_polygon(0,0,1,1,2,2, 40,40)
        #self.canvas.create_rectangle(50, 25, 150, 75)
        
        x = (self.spectrometer.capture_height)/2
        y = (self.spectrometer.capture_height)/2
        w = self.spectrometer.capture_width
        h = self.spectrometer.capture_height
        self.canvas.create_rectangle(self.spectrometer.camera.res_x/2-self.spectrometer.capture_width/2, self.spectrometer.camera.res_y/2-self.spectrometer.capture_height/2, w, h)
        #self.canvas.create_rectangle(x,y,w,h)
        print "X:%s, Y:%s, W:%s, H:%s",x, y, w, h
        #0,0 is top left
        #left_offset, top_offset, width, height
        #self.canvas.create_rectangle(10,30,630,470,fill="yellow")
      
       

        #self.bind("<Button-1>", )
        #self.pack()
        

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

