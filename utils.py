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


'''
Multiple data points may have the same wavelength, in such a case the data points
should be combined into one, with their intensities added togethe.
'''
def calc_intensities(wavelengths, intensities):
    currentWavelength = 430
    
    increment = 2

    values = {}

    while currentWavelength < 650:
        for i,wavelength in enumerate(wavelengths):
            if wavelength > currentWavelength and wavelength < currentWavelength + increment:
               values[currentWavelength + (increment / 2)] = values.get(currentWavelength + (increment / 2),1) + 1
        currentWavelength += increment

    wavelengths = []
    intensities = []
    for k,v in values.items():
        wavelengths.append(k)
        intensities.append(v)
    return [wavelengths, intensities]

