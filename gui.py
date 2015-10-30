import Tkinter
from Tkinter import *
from Tkinter import Tk
from Tkinter import Button
from picamera import PiCamera
from plotting import *
from picamera import array
import time
import cv2
import Image
import ImageTk
import numpy as np
import sys
#************** Utility Functions *****************#
    
'''
Return of shape , nrows, ncols,
where n = nrows * ncols = arr.size
'''
def blockshaped(arr, nrows, ncols):
    h, w = arr.shape
    return (arr.reshape(h//nrows, nrows, -1, ncols).swapaxes(1,2).reshape(-1, nrows, ncols))

'''
Make sure the spacing on the graph is ok to use.
'''
def check_spacing(min, max, spacing):
    if ((float)(max - min)/spacing).is_integer:
        print "Graph x spacing verified"
        return
    else:
        print "Graph x spacing invalid"
        sys.exit(0)
        return #Dead code

def make_comparator(comparator):
    def compare(x,y):
        if comparator(x,y):
            return -1
        elif comparator(y,x):
            return 1
        else:
            return 0
    return compare

def wavelength_comparator(x, y):
        wx = x[0]
        wy = y[0]
        if wx < wy:
            return True
        else:
            return False

def calc_intensities(labels, wavelength_intensities, scale = False):
    intensities = [0]*len(labels)
    for wi in wavelength_intensities:
        #Find the position on the graph where the intensity belongs
        #print "Looking for wavelength " + str(wi[0])
        try:
            p = labels.index(wi[0])
            #Add the intensity into the new intensities array at the correct location
            intensities[p] += wi[1]
        except ValueError:
            continue
    if scale:
        #Scale so that the maximum intensity is 100
        max_intensity = (255+255+255)*len(wavelength_intensities)
        intensities = [a/max_intensity for a in intensities]
        
    return intensities
        

class SpectrometerGUI(Tkinter.Tk):
    def __init__(self):
        self.res_x = 640 #Width
        self.res_y = 480 #Height
        self.capture_width = self.res_x
        self.capture_height = 2

        #Define wavelengths of colours
        self.violetwave = 380 #not sure
        self.bluewave = 440
        self.cyanwave = 490
        self.greenwave = 510
        self.yellowwave = 580
        self.redwave = 687

        #Define properties of graph
        self.x_min_range = 380
        self.x_max_range = 750
        self.x_spacing = 1
        #Ensure the spacing is compatibe with the range
        check_spacing(self.x_min_range, self.x_max_range, self.x_spacing)
        
        #self.__capture_area = self.calculate_capture_area(return_tuple=False)
         
        
        Tkinter.Tk.__init__(self)
        
        self.title = "Heriot-Watt University Pi Spectrometer"
        Tkinter.Tk.wm_title(self, self.title)
        
        logo = Tkinter.PhotoImage(file = "img/logo/favicon32.png")
        self.tk.call('wm', 'iconphoto', self._w, logo)
    
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
        


    
        
        
    def calc_x_axis(self):
        #Convert the intensity and wavelength arrays into a suitable format for the graph
        x_values = []
        number_of_points = (self.x_max_range - self.x_min_range)/self.x_spacing
        for i in range(0, number_of_points):
            x_values.append(self.x_min_range + (i*self.x_spacing))
        return x_values

    def calc_y_axis(self, x_labels, wavelength_intensities):
        #An array of size len(x_labels),
        #containing the intensity value (0 - 100) for the particular wavelength.
        
        print "unordered intensities"
        print wavelength_intensities
        
        wavelength_intensities.sort(make_comparator(wavelength_comparator))
        
        print "Ordered intensities"
        print wavelength_intensities
        
        #for wi in wavelength_intensities:
            
        return 0

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

        #Draw image on canvas
        #imgFromArray = Image.fromarray(img2)
        #imgtk = ImageTk.PhotoImage(image=imgFromArray)
        #self.canvas.create_image(self.res_x/2, self.res_y/2, image = imgtk)
        
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
        flipped = np.rot90(trimmedheight)
        averaged_array = []
        intensities = []
        wavelengths = []
        #these are all estimates
        
        for col in flipped:
            avr = 0
            avg = 0
            avb = 0
            wavelength = 0.0
            intensity = 0.0
            for pix in col:
                avr += pix[0]
                avg += pix[1]
                avb += pix[2]
            #Average the pixels in each column
            avr = avr/len(col)
            avg = avg/len(col)
            avb = avb/len(col)
            intensity = (avr + avg + avb)
            intensities.append(intensity)
            wavelength = self.colour_to_wavelength(avr, avg, avb)
            #print [avr, avg, avb, intensity, wavelength]
            averaged_array.append([avb, avg, avr])
            wavelengths.append([wavelength, intensity])
            #print wavelengths
       # print averaged_array
        #print len(averaged_array)
        
        x_values = self.calc_x_axis()
        y_values = calc_intensities(x_values, wavelengths)
        
        barplot(x_values, y_values)
        #print flipped

        #trimmedwidth = np.dsplit(trimmedheight, 3)
        #print "Height: " + str(len(trimmedwidth[0]))
        #print "Width: " + str(len(trimmedwidth[0][0]))
        camera.close()

    def colour_to_wavelength(self, avr, avg, avb):
        #Try to approximate the wavelengths of colours in each pixel
        #if between violet and blue
        if(avr > avg and avb > avg and avb > avr):
            wavelength = (avr/(avr+avb))*(self.bluewave-self.violetwave) + self.violetwave
        #if between blue and cyan
        elif(avg > avr and avb > avr and avb > avg):
            wavelength = (avg/(avg+avb))*(self.cyanwave-self.bluewave) + self.bluewave
        #if between cyan and green
        elif(avg > avb and avb > avr and avg > avb):
            wavelength = (avb/(avg+avb))*(self.greenwave-self.cyanwave)+ self.cyanwave
        #if betwenn green and yellow
        elif(avg > avb and avr > avb and avg > avr):
            wavelength = (avr/(avr+avg))*(self.yellowwave - self.greenwave) + self.greenwave
        #if between yellow and red
        elif(avr > avb and avg > avb and avr > avg):
            wavelength = (avg/(avr+avg))*(self.redwave- self.yellowwave) + self.yellowwave
        else: wavelength = 0
        return wavelength
        
if __name__ == "__main__":
    app = SpectrometerGUI()
    app.mainloop()

