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
from threading import Thread

class SpectrometerGUI(Tkinter.Tk):
    def __init__(self, spectrometer):
             
        self.spectrometer = spectrometer
       
        #Define properties of graph
        self.x_min_range = 430
        self.x_max_range = 650
        self.box_width = self.spectrometer.camera.res_x - 100
        self.box_height = 5
        self.box_x = 50
        self.box_y = self.spectrometer.camera.res_y/2 - self.box_height/2
        
        
         
        
        Tkinter.Tk.__init__(self)
        
        Tkinter.Tk.wm_title(self, "Heriot-Watt University Pi Spectrometer")

        
        
        logo = Tkinter.PhotoImage(file = "img/logo/favicon32.png")
        self.tk.call('wm', 'iconphoto', self._w, logo)
    
        
        self.canvas = Canvas(self, width = self.spectrometer.camera.res_x, height = self.spectrometer.camera.res_y, bg="white")
        self.canvas.grid(row = 0, column = 0)
        self.image = self.spectrometer.camera.get_image()
        b,g,r = cv2.split(self.image)
        img2 = cv2.merge((r,g,b))
        imgFromArray = Image.fromarray(img2)
        self.tk_image = ImageTk.PhotoImage(image=imgFromArray)
        self.image_on_canvas = self.canvas.create_image(self.spectrometer.camera.res_x/2, self.spectrometer.camera.res_y/2, image = self.tk_image)
       
        self.rectangle = self.canvas.create_rectangle(self.box_x, self.box_y, self.box_x + self.box_width, self.box_y + self.box_height, outline='white')


        f = Frame(self)
        f.grid(row = 1, column = 0)

        f1 = Frame(f)
        f1.grid(row = 0, column = 0)

        
        analyseButton = Button(f1, text = "Analyse", bg  = "blue", command = lambda : self.buttonClicked())
        analyseButton.grid(column=0, row=0)



        f2 = Frame(f)
        f2.grid(row = 0, column = 1)

        xPositionPlusButton = Button(f2, text = "Right", command = lambda : self.changeXPosition(1))
        xPositionPlusButton.grid(column=2, row=1)
        xPositionMinusButton = Button(f2, text = "Left",  command = lambda : self.changeXPosition(-1))
        xPositionMinusButton.grid(column=0, row=1)
        yPositionPlusButton = Button(f2, text = "Up",  command = lambda : self.changeYPosition(-1))
        yPositionPlusButton.grid(column=1, row=0)
        yPositionMinusButton = Button(f2, text = "Down", command = lambda : self.changeYPosition(1))
        yPositionMinusButton.grid(column=1, row=2)
        



        f3 = Frame(f)
        f3.grid(row = 0, column = 2)
        
        widthPlusButton = Button(f3, text = "Increase",  command = lambda : self.changeWidth(1))
        widthPlusButton.grid(column=0, row=0)
        widthMinusButton = Button(f3, text = "Decrease",  command = lambda : self.changeWidth(-1))
        widthMinusButton.grid(column=0, row=2)
        heightPlusButton = Button(f3, text = "Increase",  command = lambda : self.changeHeight(1))
        heightPlusButton.grid(column=2, row=0)
        heightMinusButton = Button(f3, text = "Decrease",  command = lambda : self.changeHeight(-1))
        heightMinusButton.grid(column=2, row=2)
        resetButton = Button(f3, text = "Reset", bg = 'red', command = lambda : self.reset())
        resetButton.grid(column=1,row = 1)
        w = Label(f3, fg = 'blue', text="Width")
        w.grid(column= 0, row = 1)
        h = Label(f3, fg = 'blue', text="Height")
        h.grid(column= 2, row = 1)

        
        
        
        
       
        self.camera_thread = Thread(target = UpdateImage, args=(0, self))
        self.camera_thread.daemon = True
        self.camera_thread.start()
        

    

    
    def buttonClicked(self):
        arg1 = 0
        self.analyse_thread = Thread(target = draw_line_graph, args=(arg1, self))
        self.analyse_thread.daemon = True
        self.analyse_thread.start()

        
    def changeWidth(self, pixels):
        self.box_width += 20*pixels
        self.box_x -= 10 * pixels
        self.updateRectangle()
        
    def changeHeight(self, pixels):
        self.box_height += 10*pixels
        self.box_y -= 5*pixels
        self.updateRectangle()
        
    def changeXPosition(self, pixels):
        self.box_x += 10*pixels       
        self.updateRectangle()
        
    def changeYPosition(self, pixels):
        self.box_y += 10*pixels        
        self.updateRectangle()
        
    def reset(self):
        self.box_width = self.spectrometer.camera.res_x - 100
        self.box_height = 5
        self.box_x = 50
        self.box_y = self.spectrometer.camera.res_y/2 - self.box_height/2
        self.updateRectangle()

    def updateRectangle(self):        
        self.canvas.delete(self.rectangle)
        self.rectangle = self.canvas.create_rectangle(self.box_x, self.box_y, self.box_x + self.box_width, self.box_y + self.box_height, outline='white')

def UpdateImage(delay, gui):
    while(True):
        gui.image = gui.spectrometer.camera.get_image()
        b,g,r = cv2.split(gui.image)
        img2 = cv2.merge((r,g,b))
        imgFromArray = Image.fromarray(img2)
        gui.tk_image = ImageTk.PhotoImage(image=imgFromArray)
        gui.canvas.itemconfig(gui.image_on_canvas, image = gui.tk_image)
        time.sleep(1)

def draw_line_graph(arg1, gui):
    wavelengths_intensities = gui.spectrometer.capture_capture_area(gui.image)
    #Sort the lists
    wavelengths, intensities = (list(t) for t in zip(*sorted(zip(wavelengths_intensities[0], wavelengths_intensities[1]))))

    Max = max(intensities) * 1.0
    intensities[:] = [x / Max for x in intensities]
    #for intensity in intensities:
    #    intensity /= max(intensities)        

    majorLocator = MultipleLocator(20)
    majorFormatter = FormatStrFormatter('%d')
    minorLocator = MultipleLocator(5)        
    
    pyplot.axis([gui.x_min_range,gui.x_max_range,0,max(intensities)])

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
    


if __name__ == "__main__":
    spectrometer = Spectrometer()
    app = SpectrometerGUI(spectrometer)
    app.mainloop()

