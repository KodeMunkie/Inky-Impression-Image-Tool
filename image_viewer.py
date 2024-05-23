#!/usr/bin/env python3

from platform import processor
import sys
import time
import image_processor

from PIL import Image
#from inky import Inky7Colour as Inky
from inky.mock import InkyMockImpression as Inky # Simulator
#from inky.auto import auto

#inky = auto(ask_user=True, verbose=True)
inky = Inky();
imPro =  image_processor.ImageProcessor()

if len(sys.argv) == 1:
    print("""
Usage: {file} image-file
""".format(file=sys.argv[0]))
    sys.exit(1)

start = time.time_ns()
image = Image.open(sys.argv[1])
resizedimage = image.resize(inky.resolution)
imPro.diffuse_image(resizedimage)
inky.set_image(resizedimage, 1)
inky.show()
end = (time.time_ns()-start)/1000000000
print(end)
input('Press RETURN to exit')
