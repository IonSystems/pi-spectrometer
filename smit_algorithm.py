'''
This algorithm was taken from a An RGB to Spectrum Conversion for
Reflectances, by Brian Smits. THIS IS NOT FINISHED YET
'''
def rgb_to_wavelength(r,g,b):
    int wavelength = 0
    if(r <= g and r <= b):
        wavelength = r * white_spectrum
        if(g <= b):
            wavelength += (g - r) * cyan_spectrum
            wavelength += (b - g) * blue_spectrum
        else
            wavelength += (b - r) * cyan_spectrum
            wavelength += (g - b) * green_spectrum
    elif(g <= r and g <= b):
        wavelength = g * white_spectrum
        if(r <= b):
            wavelength += (r - r) * cyan_spectrum
            wavelength += (b - g) * blue_spectrum
        else
            wavelength += (b - r) * cyan_spectrum
            wavelength += (r - b) * green_spectrum
    else(b <= r and b <= g):
        wavelength = b * white_spectrum
        if(r <= g):
            wavelength += (r - r) * cyan_spectrum
            wavelength += (g - g) * blue_spectrum
        else
            wavelength += (b - r) * cyan_spectrum
            wavelength += (g - b) * green_spectrum
    return wavelength
