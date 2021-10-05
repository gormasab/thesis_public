# Reihaneh Shahmoradi
import cv2
import matplotlib.pyplot as plt
import pyrealsense2 as rs

import functions.basics
import functions.cameraparams

item1 = (215, 434, 1717)  # R_ankle
item2 = (211,208,1549)  # R_hip
correctlength = 97
img_path = r".\data\11_22_53\RGB\RGB_32.png"


def drawline_and_projection(item1, item2, correctlength, img_path):
    img = cv2.imread(img_path)
    intr = functions.cameraparams.load_params()
    point1 = rs.rs2_deproject_pixel_to_point(intr, item1[0:2], item1[2])
    point2 = rs.rs2_deproject_pixel_to_point(intr, item2[0:2], item2[2])
    print(f"p1:{point1},p2:{point2}")
    mdist = functions.basics.eucli_dist(point1, point2)/10
    print(mdist)
    accuracy = mdist / correctlength
    if 1.05 > accuracy > 0.95:
        color = (0, 255, 0)
    elif 0.9 < accuracy < 0.95:
        color = (255, 255, 0)
    else:
        color = (255, 0, 0)

    print(accuracy)
    img = cv2.line(img, (int(item1[0]), int(item1[1])), (int(item2[0]), int(item2[1])), color)
    # cv2.line()

    plt.clf()
    return (img, mdist)


img, mdist = drawline_and_projection(item1, item2, correctlength, img_path)
plt.imshow(img)
plt.show()

""""


function((item1,item2),(correct_len,)(image)
calculates X1 Y1 Z1
            X2 Y2 Z2
mdis = eucl dist
corlen/mdis = 1 or sth

if >0.99 > 1 > 1.1
    color = green
etc

drawline(x,y)(x2,y2)(color)
return (image,mdis)
"""
