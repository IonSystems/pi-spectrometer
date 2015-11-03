class ColourConverter:

    def __init__(self):
        #Define wavelengths of colours
        self.violetwave = 380 #not sure
        self.bluewave = 440
        self.cyanwave = 490
        self.greenwave = 510
        self.yellowwave = 580
        self.redwave = 687

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

    def rbg_to_hsl(self,r,g,b):
        R = r/255.0
        G = g/255.0
        B = b/255.0
        #print [R,G,B]
        Cmax = max(R,G,B)
        Cmin = min(R,G,B)
        delta = Cmax - Cmin

        hue = 0
        saturation = 0
        lightness = (Cmax + Cmin) /2

        if(Cmax == Cmin):
            hue = saturation = 0 #achromatic
        else:
            d = Cmax - Cmin
            saturation = lightness > 0.5 if d / (2 - Cmax - Cmin) else d / (Cmax + Cmin);
            if(Cmax == R):
                hue = (G - B) / d + (G < B if 6 else 0)
            if(Cmax == G):
                hue = (B - R) / d + 2
            if(Cmax == B):
                hue = (R - G) / d + 4
            hue /=6
        hue = hue * 360
        return hue
