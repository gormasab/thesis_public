# Reihaneh Shahmoradi
import os
import pickle
import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy import ndimage

from functions.create_table import tablemaker
from functions.syscheck import iswindows as isw
import functions.basics as myfuncs
from functions.plotthings import plotmaker as plotmaker

project_folder = "20_20_28"
path_KP = isw("./data/" + project_folder + "/Keypoints/")
path_depth = isw("./data/" + project_folder + "/Depth/")
path_RGB = isw("./data/" + project_folder + "/RGB/")

RGB_filename = "RGB_"
depth_filename = "dfile_"
kp_filename = "kp_"

keylist = ['nose', 'chest', 'R_shoulder', 'R_elbow', 'R_hand', 'L_shoulder', 'L_elbow',
           'L_hand', 'hip', 'R_hip', 'R_knee', 'R_ankle', 'L_hip', 'L_knee', 'L_ankle',
           'R_eye', 'L_eye', 'R_ear', 'L_ear', 'L_foot2', 'L_foot3', 'L_foot4', 'R_foot2',
           'R_foot3', 'R_foot4']
truelist = [21,  # 'chest', 'R_shoulder'
            32,  # 'R_shoulder', 'R_elbow'
            32,  # 'R_elbow', 'R_hand'
            21,  # 'chest', 'L_shoulder'
            32,  # 'L_shoulder', 'L_elbow'
            32,  # L_elbow', 'L_hand'
            15,  # 'hip', 'R_hip'
            52,  # 'R_hip', 'R_knee'
            45,  # 'R_knee', 'R_ankle'
            15,  # 'hip', 'L_hip'
            52,  # 'L_hip', 'L_knee'
            45]  # 'L_knee', 'L_ankle'
truelistarray = np.array(truelist)
combolist = [('chest', 'R_shoulder'), ('R_shoulder', 'R_elbow'), ('R_elbow', 'R_hand'), ('chest', 'L_shoulder'),
             ('L_shoulder', 'L_elbow'), ('L_elbow', 'L_hand'), ('hip', 'R_hip'), ('R_hip', 'R_knee'),
             ('R_knee', 'R_ankle'), ('hip', 'L_hip'), ('L_hip', 'L_knee'), ('L_knee', 'L_ankle')]

drawcolor = False  # draws the keypoints on the RGB image (debug tool)
drawdepth = False  # draws the keypoints on the depth image (debug tool)
plotting = False  # shows a plot of all the joint-pairs on the RGB image (colored:accuracy)
save_params = True  # saves the 'frames' and 'sdb' variables
timeseries = True
filter = "gaussian"

kp_list = os.listdir((isw("./data/" + project_folder + "/Keypoints/")))
asdf = []


def getnumber(my_str):
    start = my_str.find("_")
    end = my_str.find(".")
    return int(my_str[start + 1:end])


sortkp = sorted(kp_list, key=getnumber)

if __name__ == "__main__":
    joint_pair_distance = []  #
    xydepth_list = []

    for iterator in range(getnumber(sortkp[0]), getnumber(sortkp[-1])):
        print(iterator)
        # point_dict is a dictionary containing (x,y,depth) with the key value being the name
        # of the joint
        point_dict = {}  # should be INSIDE the for loop.
        # list of distance between joint-pairs
        distance_list = []  # big problems if u introduce it outside for loop

        # this can be done better using os.listdir, but requires some preprocessing.
        # maybe later?
        path_keypoints = path_KP + kp_filename + repr(iterator) + ".txt"
        path_depthfile = path_depth + depth_filename + repr(iterator) + ".txt"

        with open(path_keypoints) as file_kp:
            keypoints = np.loadtxt(file_kp)

        with open(path_depthfile) as file_depth:
            # file_depth2 = str(file_depth)
            depth_load = np.loadtxt(file_depth)

        myim = cv2.imread(path_RGB + RGB_filename + str(iterator) + ".png")
        myim = cv2.cvtColor(myim, cv2.COLOR_BGR2RGB)
        myim_copy = np.copy(myim)

        """"
        Which depth_filter will be used today?
        """
        if filter == "nofilter":
            depth_load_filter = depth_load
        if filter == "bilateral":
            depth_load_filter = myfuncs.filtered_img(depth_load, 'bilateral')
        if filter == "median":
            depth_load_filter = ndimage.median_filter(depth_load, size=100)
        if filter == "gaussian":
            depth_load_filter = ndimage.gaussian_filter(depth_load, sigma=100)

        """"
        Keypoints are 25,3 (currently, 25 could change) first val: X, second, Y, third 
        certainty)  
        """
        testarrayX = keypoints[:, 0]
        testarrayY = keypoints[:, 1]

        # !!!!! IMPORTANT
        # ROW COLUMN =! X,Y
        # ROW COLUMN IS Y,X

        for x, y, key in zip(testarrayX, testarrayY, keylist):
            x = int(round(x))
            y = int(round(y))

            depth = depth_load_filter[y, x]
            point_dict[key] = (x, y, depth)

            """"
            Drawcolor and drawdepth are debugging tools. They show the position of each keypoint
            step by step.
            """
            if drawcolor is True:
                # we can give X,Y because color_ting switches the row/column thing already
                colored_im = myfuncs.color_ting(myim_copy, [0, 255, 0], [x, y])
                plt.imshow(colored_im)
            if drawdepth is True:
                colored_im = myfuncs.color_ting(myim_copy, [2 ** 16], [x, y])
                plt.imshow(colored_im)
            if drawdepth | drawcolor is True:
                plt.show()

        xydepth_list.append(point_dict)

        """"
        Section creates joint-pairs. Then tales in x,y,depth for joint pair,
        and uses X,Y,Z to calculate the euclidian distance. This distance
        """
        for keys, truevalue in zip(combolist, truelist):
            item = [tuple, tuple]
            for key, it in zip(keys, [0, 1]):
                n = 0
                while xydepth_list[iterator - n][key][2] == 0:
                    # while depth value is zero, go one frame back until the value is nonzero
                    n += 1
                item[it] = xydepth_list[iterator - n][key]

            myim, mydist = myfuncs.drawline_and_deprojection(item[0], item[1], truevalue, myim)
            distance_list.append(mydist)

        # joint_pair_distance is the list of distances between each joint-pair, over every
        # frame!
        joint_pair_distance.append(distance_list)
        # now joint_pair_distance is

        if plotting:
            myim = cv2.cvtColor(myim, cv2.COLOR_BGR2RGB)
            # depth_image_3d = np.dstack((depth_load, depth_load, depth_load))
            depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_load_filter, alpha=0.03), cv2.COLORMAP_SPRING)
            images = np.hstack((myim, depth_colormap))

            cv2.imshow("cv window", images)
            cv2.waitKey(1)

    # # # # # # # # #
    # END FOR LOOP
    # # # # # # # # #

    bias, sd = myfuncs.calc_sdb(joint_pair_distance, truelistarray)
    fp = isw("./data/" + project_folder + "/results/")

    if save_params:
        if not os.path.exists(fp):
            os.mkdir(fp)
        # write joint pair distance
        file = open(fp + "jpd.pcl", 'wb')
        pickle.dump(joint_pair_distance, file)
        file.close()
        # write bias/std
        file = open(isw(fp + "bsd.pcl"), 'wb')
        pickle.dump([bias, sd], file)
        file.close()

    if timeseries:
        fp += isw("timeseries/")
        if not os.path.exists(fp):
            os.mkdir(fp)
        fp += isw(filter + "/")
        if not os.path.exists(fp):
            os.mkdir(fp)
        plotmaker(joint_pair_distance, sd, fp,combolist,truelist,filter)

    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    tablemaker(truelist, bias, sd)
