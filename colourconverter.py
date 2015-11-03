class ColourConverter:

          

   
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
        return [hue, saturation]
