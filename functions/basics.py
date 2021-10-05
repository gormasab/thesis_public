import os
import statistics
import cv2
import numpy as np
import pyrealsense2 as rs
from scipy import ndimage
from scipy.ndimage import gaussian_filter
from scipy.signal import wiener

import functions.cameraparams


def scale_im(img, maxdist):
    """
    This function filters out high distances

    :param img:
    :return:
    """
    s_factor = np.floor(2 ** 16 / maxdist)

    temp = np.where(img > maxdist, maxdist, img * s_factor)

    image = np.reshape(temp, (480, 640))
    return image.astype('uint16')


def max_dist(img, maxdist):
    # remember histogram equalization
    t_max = 2 ** 16  # uint16
    s_factor = np.floor(t_max / maxdist)
    image = np.where(img > maxdist, t_max, img * s_factor)
    return image.astype('uint16')


def get_files(path):
    a = os.listdir(path)
    # print(a)
    return a


def create_folder(pathway):
    yorno = os.path.exists(pathway)
    if not yorno:
        os.mkdir(pathway)
        os.mkdir(pathway + "/RGB/")
        os.mkdir(pathway + "/Depth/")
        os.mkdir(pathway + "/Keypoints/")
    else:
        raise Exception("File already exists!!")

    return


# imported from backprojection

def color_ting(img, color, coords):
    """
    This function DRAWS A SQAURE ON THE IMAGE
    """
    X = coords[0]
    Y = coords[1]
    # print(img.shape)
    # ROW COLUMN = [Y, X]
    img[Y - 5:Y + 5, X - 5:X + 5] = color
    return img


def eucli_dist(point1, point2):
    """
    This function measures the distance between 2 points in 3d space
    """
    termx = (point1[0] - point2[0]) ** 2
    termy = (point1[1] - point2[1]) ** 2
    termz = (point1[2] - point2[2]) ** 2
    return np.sqrt(termx + termy + termz)


def eucli_2d(point1, point2):
    """
    This function measures the distance between 2 points in 2d space
    """
    termx = (point1[0] - point2[0]) ** 2
    termy = (point1[1] - point2[1]) ** 2
    return np.sqrt(termx + termy)


def drawline_and_deprojection(item1, item2, correctlength, img_path):
    """
    :param item1: a part of joints
    :param item2: another part of joints
    :param correctlength: measured the correct length
    :param img_path: path of the image
    :return: measured distance, using euclidian distance between points in 3D space (backprojected)
    """
    if isinstance(img_path, str):
        img = cv2.imread(img_path)
    elif isinstance(img_path, np.ndarray):
        img = img_path
    else:
        raise ValueError("enter string or ndarray as IMGPATH!!!!!!!!")

    intr = functions.cameraparams.load_params()
    point1 = rs.rs2_deproject_pixel_to_point(intr, item1[0:2], item1[2])
    point2 = rs.rs2_deproject_pixel_to_point(intr, item2[0:2], item2[2])

    mdist = functions.basics.eucli_dist(point1, point2) / 10
    accuracy = mdist / correctlength
    upper_sth = 1.15
    upper_max = 1.05
    lower_max = 0.95
    bad = 0.85

    if upper_max > accuracy > lower_max:
        color = (0, 255, 0)
        # tp=tp+1
    elif bad < accuracy < lower_max:
        color = (255, 255, 0)
    elif upper_max < accuracy < upper_sth:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)

    img = cv2.line(img, (int(item1[0]), int(item1[1])), (int(item2[0]), int(item2[1])), color)

    return img, mdist


def filtered_img(image: np.ndarray, filter_type: str):
    if filter_type == 'median':
        result = ndimage.median_filter(image, 15)
    elif filter_type == 'gaussian':
        result = gaussian_filter(image, sigma=15)
    elif filter_type == 'wiener':
        result = wiener(image, 35)

        """
        Mysize:  A scalar or an N-length list giving the size of the Wiener filter window
                    in each dimension. Elementsof mysize should be odd. If mysize is a scalar, then this
                    scalar is used as the size in each dimension.
        Noise:   The noise-power to use. If None, then noise is estimated as the average of the local
                    variance of the input.           
        """

    elif filter_type == 'bilateral':
        # image = np.uint8(image)
        image = np.float32(image)
        result = cv2.bilateralFilter(image, 5, 20, 20)

        """"
        Sigma values: For simplicity, you can set the 2 sigma values to be the same. If they are small (< 10),
        the filter will not have much effect, whereas if they are large (> 150), they will have
        a very strong effect, making the image look "cartoonish".

        Filter size: Large filters (d > 5) are very slow, so it is recommended to use d=5
        for real-time applications, and perhaps d=9 for offline applications that need heavy
        noise filtering.
        
        src:	    Source 8-bit or floating-point, 1-channel or 3-channel image.
        dst:	    Destination image of the same size and type as src .
        d:  	    Diameter of each pixel neighborhood that is used during filtering. If it is
                    non-positive, it is computed from sigmaSpace.
        sigmaColor:	Filter sigma in the color space. A larger value of the parameter means
                    that farther colors within the pixel neighborhood (see sigmaSpace) will be mixed
                    together, resulting in larger areas of semi-equal color.
        sigmaSpace:	Filter sigma in the coordinate space. A larger value of the parameter means
                    that farther pixels will influence each other as long as their colors are
                    close enough (see sigmaColor ). When d>0, it specifies the neighborhood
                    size regardless of sigmaSpace. Otherwise, d is proportional to sigmaSpace.
        """
    else:
        result = "you did not choose a correct filter"
        raise Exception("wrong filter choice")
    return result


def calc_sdb(biglist, truelistarray):
    big_length = len(biglist)
    small_length = len(biglist[0])
    longlist = []

    for item in biglist:
        for number in item:
            longlist.append(number)

    all_keypoints = []

    for i in range(small_length):
        # keypoint loop
        keypoints = []
        for j in range(big_length):
            # frame loop
            keypoints.append(longlist[i + small_length * j])

        all_keypoints.append(keypoints)

    meanz = []

    for element in all_keypoints:
        meanz.append(statistics.mean(element))

    keypoint_array = np.array(all_keypoints)
    meanzarray = np.array(meanz)

    bias = abs(truelistarray - meanzarray)
    #print({'Normal': [bias]})
    sd = []

    for element in keypoint_array:
        sd.append(statistics.stdev(element))

    #print(sd)

    return bias,sd
