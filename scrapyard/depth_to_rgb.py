""""
This
"""

# from PIL import Image
import matplotlib.pyplot
import numpy as np


def makergb(img: np.ndarray):
    # incoming image is (normally) uint16
    the_size = img.shape
    newim = np.zeros((*the_size, 3), dtype='float64')
    for element in range(3):
        newim[:, :, element] = img / 6000
    return newim

def un_rgb(img: np.ndarray):
    the_size = img.shape
    newim = np.zeros((the_size[0],the_size[1]), dtype='uint16')
    newim[::] = img[::1]
    newim *= 6000
    return newim


if __name__ == "__main__":
    current_time = "13_22_41"
    dlist = []

    for iterator in range(1, 10):
        path_depthfile = ".\\data\\" + current_time + "\\Depth\\dfile_" + str(iterator) + ".txt"
        with open(path_depthfile) as file_depth:
            # file_depth2 = str(file_depth)
            depth_load = np.loadtxt(file_depth, dtype='uint16')
        rgbim = makergb(depth_load)
        dlist.append(rgbim)

    matplotlib.pyplot.imshow(dlist[2])
    matplotlib.pyplot.show()
