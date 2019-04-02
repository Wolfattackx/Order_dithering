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



def dither(pixel, width, height, colorfactor):

    Npixel = pixel
    print(pixel[0][0])
    print(Npixel[0][0])

    for y in range(0, width - 1):
        for x in range(1, height - 1):
            oldpixel_r, oldpixel_g, oldpixel_b = Npixel[x][y]

            newpixel_r = int((colorfactor * oldpixel_r / 255)) * int((255 / colorfactor))
            newpixel_g = int((colorfactor * oldpixel_g / 255)) * int((255 / colorfactor))
            newpixel_b = int((colorfactor * oldpixel_b / 255)) * int((255 / colorfactor))
            
            Npixel[x][y] = (newpixel_r, newpixel_g, newpixel_b)

            quant_error_r = oldpixel_r - newpixel_r
            quant_error_g = oldpixel_g - newpixel_g
            quant_error_b = oldpixel_b - newpixel_b

            dither_R = float(Npixel[x + 1][y][0] + quant_error_r * (7.0 / 16.0))
            dither_G = float(Npixel[x + 1][y][1] + quant_error_g * (7.0 / 16.0))
            dither_B = float(Npixel[x + 1][y][2] + quant_error_b * (7.0 / 16.0))

            Npixel[x + 1][y] = (dither_R, dither_G, dither_B)
            
            dither_R = float(Npixel[x - 1][y + 1][0] + quant_error_r * (3.0 / 16.0))
            dither_G = float(Npixel[x - 1][y + 1][1] + quant_error_g * (3.0 / 16.0))
            dither_B = float(Npixel[x - 1][y + 1][2] + quant_error_b * (3.0 / 16.0))

            Npixel[x - 1][y + 1] = (dither_R, dither_G, dither_B)

            dither_R = float(Npixel[x][y + 1][0] + quant_error_r * (5.0 / 16.0))
            dither_G = float(Npixel[x][y + 1][1] + quant_error_g * (5.0 / 16.0))
            dither_B = float(Npixel[x][y + 1][2] + quant_error_b * (5.0 / 16.0))

            Npixel[x][y + 1] = (dither_R, dither_G, dither_B)

            dither_R = float(Npixel[x + 1][y + 1][0] + quant_error_r * (1.0 / 16.0))
            dither_G = float(Npixel[x + 1][y + 1][1] + quant_error_g * (1.0 / 16.0))
            dither_B = float(Npixel[x + 1][y + 1][2] + quant_error_b * (1.0 / 16.0))

            Npixel[x + 1][y + 1] = (dither_R, dither_G, dither_B)
            print(Npixel[x][y])
    
    return Npixel


def LoadPixel(imagepath, colorfactor):
    im = Image.open(imagepath, 'r')
    width, height = im.size

    pixel = np.array(im.convert("L"))
    pixel.setflags(write = 1)

    print("The size of the image is: {}x{}".format(width, height))

    im2 = Image.fromarray(order_dither(pixel, height, width))
    #im2 = Image.fromarray(dither(pixel, width, height, colorfactor))

    im2.save('out.png')

    im2.close()
    im.close()


def main():
    if(len(sys.argv) != 3):
        print("Usage {} 'colorfactor' <Path to the image file>".format(sys.argv[0]))

    else:
        LoadPixel(sys.argv[2], int(sys.argv[1]))
        

if __name__ == '__main__':
    main()
    input("Press anything to quit......")
