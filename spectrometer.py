from camera import Camera
from colourconverter import ColourConverter
import numpy as np

import utils

class Spectrometer:
    def __init__(self):
        self.camera = Camera()
        self.colourconverter = ColourConverter()
        self.capture_width = self.camera.res_x
        self.capture_height = 10
        
    def capture_capture_area(self, img):
        #camera = PiCamera()
        #camera.resolution = (self.res_x, self.res_y)
        #capture = array.PiRGBArray(camera)
        #camera.capture(capture, format = "bgr")
        #img = capture.array
        #img = self.camera.get_image()

        #Draw image on canvas
        #imgFromArray = Image.fromarray(img2)
        #imgtk = ImageTk.PhotoImage(image=imgFromArray)
        #self.canvas.create_image(self.res_x/2, self.res_y/2, image = imgtk)
        
        height = len(img)
        width = len(img[0])
        #print blockshaped(img, 2, 640)
        
        #The amount of rows to be removed from the top
        remove_top = (self.camera.res_x - self.capture_height)/2
        
        #The amount of rows to be kept, after the above has been removed.
        keep_middle = self.capture_height
        
        trimmedheight = img[remove_top:] #Remove first x rows
        trimmedheight = trimmedheight[:keep_middle] #Keep first x rows
        print "Height: " + str(len(trimmedheight))
        print "Width: " + str(len(trimmedheight[0]))

        #Flip the array so we can iterate through each column
        flipped = np.rot90(trimmedheight)
        averaged_array = []
        intensities = []
        wavelengths = []
        #these are all estimates
        
        for col in flipped:
            avr = 0
            avg = 0
            avb = 0
           
            
            
            for pix in col:
                avr += pix[2]
                avg += pix[1]
                avb += pix[0]
                
            #Average the pixels in each column
            avr = avr/len(col)
            avg = avg/len(col)
            avb = avb/len(col)
            intensity = avr + avg + avb / 3
            
            hue_lightness = self.colourconverter.rbg_to_hsl(avr, avg, avb)
            
            scaled_hue = -hue_lightness[0] * (22.0/27.0) 
            wavelength = scaled_hue + 650.0
            
            print [avr, avg, avb, wavelength]
            
            wavelengths.append(wavelength)
            intensities.append(hue_lightness[1])
            #print wavelengths
       # print averaged_array
        #print len(averaged_array)
        calded = utils.calc_intensities(wavelengths, intensities)
        return calded
        #print flipped

        #trimmedwidth = np.dsplit(trimmedheight, 3)
        #print "Height: " + str(len(trimmedwidth[0]))
        #print "Width: " + str(len(trimmedwidth[0][0]))
        #camera.close()

    def calculate_capture_area(self, return_tuple = True):
        #TODO: Check if we chould be using the bottom left as 0,0
        #Assuming bottom left is 0,0

        #Work out bottom left corner and work from there.
        b_x = (self.spectrometer.camera.res_x - self.capture_height) / 2
        l_y = (self.spectrometer.camera.res_y - self.capture_width) / 2

        t_x = b_x + self.capture_height
        r_y = l_y + self.capture_width
        
        if return_tuple:
            return {'top':t_x, 'bottom':b_x, 'left':l_y, 'right':r_y}
        #TODO return in another format?
        else:
            return [b_x, l_y, t_x, l_y, t_x, r_y, b_x, r_y]
