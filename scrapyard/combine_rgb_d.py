# Reihaneh Shahmoradi

import json

import cv2
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

my_mean = []

""""
NEW version of Combine.py

This function combines a depth.txt file with a RGB image. Then it takes pre-generated keypoints stored in
a JSON file. It then tries to compute distance and calculate a pixel/mm ratio. However, due to backprojection not
being implemented there are inaccuracies.


asasi5:             RGB images
asasi5-result:      keypoints JSON from OPENPOSE
asasi6:             depth results (txt)
"""


def color_ting(img, color, coords):
    X = coords[0]
    Y = coords[1]
    img[Y - 5:Y + 5, X - 5:X + 5] = color
    return img


def eucli_dist(point1,point2):
    termx = (point1[0]-point2[0])**2
    termy = (point1[1]-point2[1])**2
    termz = (point1[2]-point2[2])**2
    return np.sqrt(termx+termy+termz)


def eucli_2d(point1,point2):
    termx = (point1[0]-point2[0])**2
    termy = (point1[1]-point2[1])**2
    return np.sqrt(termx+termy)


for iterator in range(30, 31):

    path_json = "./asasi5-result/." + repr(iterator) + "_keypoints.json"
    path_depth = "./asasi6/." + repr(iterator) + ".txt"

    # reading and correctly closing the json
    with open(path_json) as file_json:
        data = json.load(file_json)

    # same for the depth file
    with open(path_depth) as file_depth:
        depth_load = np.loadtxt(file_depth)

    keypoints = data['people'][0]['pose_keypoints_2d']
    kp_coords = []

    # we take the keypoints, and disregard every third element (i.e. the uncertainty,
    # such that we are left with only the [x,y] coordinates. We add from the depth image
    # the Z coordinate too.
    for element in range(len(keypoints)):
        if element % 3 == 0:
            x = round(keypoints[element])
            y = round(keypoints[element + 1])
            z = depth_load[x, y]
            kp_coords.append([x, y, z])

    # So now we have 'kp_coords' which is equal to ff

    img = cv2.imread(r'.\asasi7\.' + repr(iterator) + '.png')
    red = [255, 0, 0]

    for element in kp_coords:
        x = element[0]
        y = element[1]
        img[y - 5:y + 5, x - 5:x + 5] = red
        cv2.imwrite("./results/image" + repr(iterator) + ".png", img)

    imgplot = plt.imshow(img)
    plt.show()

    ff = kp_coords

    table = [['Number', 'Part of the body', 'x', 'y', 'z']
        , [0, 'nose', ff[0][0], ff[0][1], ff[0][2]]
        , [1, 'chest', ff[1][0], ff[1][1], ff[1][2]]
        , [2, 'R shoulder', ff[2][0], ff[2][1], ff[2][2]]
        , [3, 'R elbow', ff[3][0], ff[3][1], ff[3][2]]
        , [4, 'R hand', ff[4][0], ff[4][1], ff[4][2]]
        , [5, 'l shoulder', ff[5][0], ff[5][1], ff[5][2]]
        , [6, 'l elbow ', ff[6][0], ff[6][1], ff[6][2]]
        , [7, 'l hand', ff[7][0], ff[7][1], ff[7][2]]
        , [8, 'hip', ff[8][0], ff[8][1], ff[8][2]]
        , [9, 'R hip', ff[9][0], ff[9][1], ff[9][2]]
        , [10, 'R knee', ff[10][0], ff[10][1], ff[10][2]]
        , [11, 'R ankle', ff[11][0], ff[11][1], ff[11][2]]
        , [12, 'l hip', ff[12][0], ff[12][1], ff[12][2]]
        , [13, 'l knee', ff[13][0], ff[13][1], ff[13][2]]
        , [14, 'l ankle', ff[14][0], ff[14][1], ff[14][2]]
        , [15, 'R eye', ff[15][0], ff[15][1], ff[15][2]]
        , [16, 'l eye', ff[16][0], ff[16][1], ff[16][2]]
        , [17, 'R ear', ff[17][0], ff[17][1], ff[17][2]]
        , [18, 'l ear', ff[18][0], ff[18][1], ff[18][2]]
        , [19, 'l foot-2', ff[19][0], ff[19][1], ff[19][2]]
        , [20, 'l foot-3', ff[20][0], ff[20][1], ff[20][2]]
        , [21, 'l foot-4', ff[21][0], ff[21][1], ff[21][2]]
        , [22, 'R foot-2', ff[22][0], ff[22][1], ff[22][2]]
        , [23, 'R foot-3', ff[23][0], ff[23][1], ff[23][2]]
        , [24, 'R foot-4', ff[24][0], ff[24][1], ff[24][2]]
             ]

    print(tabulate(table))

    # green = [0, 255, 0]
    # blue = [0,0,255]
    # purple = [0, 255,255]
    # # color ankles
    # color_ting(img,green,ff[11][0:2])
    # color_ting(img, green, ff[14][0:2])
    # # color knees
    # color_ting(img,blue,ff[10][0:2])
    # color_ting(img,blue,ff[13][0:2])
    # # color hips
    # color_ting(img,purple,ff[12][0:2])
    # imgplot = plt.imshow(img)
    # plt.show()

    r_ankle = ff[11]
    print(f"z:Rhip {ff[9][2]}")
    r_knee = ff[10]
    print(f"z:Rknee {ff[10][2]}")

    # r_ankle_knee_distance = eucli_dist(r_ankle, r_knee)  # pixels & ??
    r_ankle_knee_distance = eucli_2d(r_ankle, r_knee)  # pixels & ??
    r_ankle_knee_measured = 43  # CM
    print(f"ankle knee distance in pixels: {r_ankle_knee_distance}")
    pixel_factor = r_ankle_knee_measured/r_ankle_knee_distance  # CM / PIXEL
    print(f"pixel factor: {pixel_factor} cm/pixel")

    l_ankle = ff[14]
    print(f"z:Lhip {ff[12][2]}")
    print(f"z:Lknee {ff[13][2]}")

    l_hip = ff[13]
    #l_ankle_hip_distance = eucli_dist(l_ankle, l_hip)
    l_ankle_hip_distance = eucli_2d(l_ankle, l_hip)
    print(f"ankle hip distance in pixels: {l_ankle_hip_distance}")
    est_length= pixel_factor*l_ankle_hip_distance
    print(f"estimated ankle hip CM: {est_length}")




#
# print(statistics.mean(my_mean))
# print(statistics.stdev(my_mean))
#
# ###why 43 would be there? unitttt?? critical?
