# Reihaneh Shahmoradi

import json
import statistics

import cv2
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate

my_mean = []

""""
asasi5:             RGB images
asasi5-result:      keypoints JSON from OPENPOSE
asasi6:             depth results (txt)
"""


for j in range(30, 31):

    # Opening JSON file
    m = open('./asasi5-result/.' + repr(j) + '_keypoints.json')
    # returns JSON object as a dictionary
    data = json.load(m)
    keypoints = data['people']

    # give keys and values
    keys, values = zip(*keypoints[0].items())
    i = 0

    a = []

    # if the index left over to 3 is 2 we continue else...
    b = []
    for i in range(0, len(values[1])):
        b.append(i % 3)
        if i % 3 == 2:
            continue
        else:
            a.append(values[1][i])

            # we have to convert it to integer
    a = [round(num) for num in a]

    rr = []
    for e in range(0, len(a), 2):
        st = a[e:e + 2]
        rr.append(st)

    # combning the depth (in txt file) with the x and y
    s = open("./asasi6/." + repr(j) + ".txt", "r")
    ss = np.loadtxt(s)

    # bb=[]
    hh = []
    ff = []

    for p in range(0, len(rr)):
        x = rr[p][0]
        y = rr[p][1]
        hh = [x, y, ss[x][y]]
        ff.append(hh)

    print(ff)

    # Show in the image
    img = cv2.imread('./asasi5/.' + repr(j) + '.png')
    imgplot = plt.imshow(img)

    for i in range(0, 24):
        x = ff[i][0]
        y = ff[i][1]
        red = [255, 0, 0]
        img[y - 5:y + 5, x - 5:x + 5] = red
        cv2.imwrite("./results/image" + repr(j) + ".png", img)
    imgplot = plt.imshow(img)
    plt.show()

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
        , [11, 'R foot-1', ff[11][0], ff[11][1], ff[11][2]]
        , [12, 'l hip', ff[12][0], ff[12][1], ff[12][2]]
        , [13, 'l knee', ff[13][0], ff[13][1], ff[13][2]]
        , [14, 'l foot-1', ff[14][0], ff[14][1], ff[14][2]]
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

    estimate = np.sqrt(((ff[11][0] - ff[10][0]) ** 2) + ((ff[11][1] - ff[10][1]) ** 2) + ((ff[11][2] - ff[10][2]) ** 2))

    print(estimate)
    ss = 43 / estimate
    print(43 / estimate)

    real2 = ss * np.sqrt(
        +((ff[14][0] - ff[12][0]) ** 2) + ((ff[14][1] - ff[12][1]) ** 2) + ((ff[14][2] - ff[12][2]) ** 2))

    print(real2)

    my_mean.append(real2)
    print(my_mean)

print(statistics.mean(my_mean))
print(statistics.stdev(my_mean))

###why 43 would be there? unitttt?? critical?
