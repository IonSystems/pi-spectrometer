import time
import picamera
import picamera.array
import numpy as np

from PIL import Image, ImageFilter
from scipy import ndimage, misc

with picamera.PiCamera() as camera:
    with picamera.array.PiBayerArray(camera) as stream:
        camera.capture(stream, 'jpeg', bayer=True)
        # Demosaic data and write to output (just use stream.array if you
        # want to skip the demosaic step)
        output = (stream.demosaic() >> 2).astype(np.uint8)
        with open('image.data', 'wb') as f:
            output.tofile(f)
        #rawData = open('image.data', 'rb').read()
        #imgSize = (100, 100)
        #img = Image.fromstring('L', imgSize, rawData, 'raw', 'F;16')
        #img.save("lalala.png")
        rawfile = np.fromfile('image.data', 'uint8')
        print len(rawfile)
        rawfile.shape = (2592, 5832)
        misc.imsave('save.png', rawfile)
