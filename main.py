from os import write
from PIL import Image
import numpy as np
from statistics import mean
import sys

if(len(sys.argv) < 1):
    print("missing arguments: must insert picture name")

im = Image.open(sys.argv[1])

def checkCloudPresence(img):
    data = np.array(img)
    height, width, _ = data.shape

    for row in range(height):
        for col in range(width):
            r, g, b = data[row, col]
            minChannelValue = min(r,g,b)
            maxChannelValue = max(r,g,b)
            
            if((maxChannelValue - minChannelValue) < 40 
                and mean([r,g,b]) > 200):
                return True

    return False

pixelNumCloud = 0

if(checkCloudPresence(im)):
    print("cloud found, analyzing...")
    posterizationImg = im.convert('P', palette=Image.ADAPTIVE, colors=6)

    postArray = np.array(posterizationImg)
    originalImageArray = np.array(im)

    originalImageArray.setflags(
        write=1
    )

    height, width = postArray.shape

    for row in range(height):
        for col in range(width):
            pixel = postArray[row][col]
            if(pixel in [0,1,2]):
                pixelNumCloud += 1 
                originalImageArray[row][col] = [0,max(originalImageArray[row][col]),0]


    im1 = Image.fromarray(originalImageArray)
    im1.save("output_" + sys.argv[1], "JPEG")
    im1.show()
    print("number of cloud pixel: "+ str(pixelNumCloud))
    print("output image: ", "output_" + sys.argv[1])
else:
    print("cloud not found closing..")
