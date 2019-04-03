#!/usr/bin/python3

import sys
from PIL import Image
import numpy as np

def order_dither(pixel, width, height):

    dithersize = 8
    dithering_lookup = [ 0, 48, 12, 60, 3, 51, 15, 63,
                        32, 16, 44, 28, 35, 19, 47, 31,
                        8,  56, 4,  52, 11, 59, 7,  55,
                        40, 24, 36, 20, 43, 27, 39, 23,
                        2,  50, 14, 62, 1,  49, 13, 61,
                        34, 18, 46, 30, 33, 17, 45, 29,
                        10, 58, 6,  54, 9,  57, 5,  53,
                        42, 26, 38, 22, 41, 25, 37, 21]

    for x in range(0, width):
        for y in range(0, height):

        	localX = x % dithersize
        	localY = y % dithersize

        	required_shade = dithering_lookup[localY + (localX * dithersize)]

        	if(pixel[x][y] <= required_shade):
        		pixel[x][y] = 50

        	else:
        		pixel[x][y] = 200

    return pixel

def LoadPixel(imagepath):
    im = Image.open(imagepath, 'r')
    width, height = im.size

    pixel = np.array(im.convert("L"))
    pixel.setflags(write = 1)

    print("The size of the image is: {}x{}".format(width, height))

    im2 = Image.fromarray(order_dither(pixel, height, width))

    im2.save('out.png')

    im2.close()
    im.close()


def main():
    if(len(sys.argv) != 2):
        print("Usage {} <Path to the image file>".format(sys.argv[0]))

    else:
        LoadPixel(sys.argv[1])
        

if __name__ == '__main__':
    main()
    input("Press anything to quit......")
