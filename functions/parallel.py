from functions.basics import calc_sdb
import functions.basics
import functions.cameraparams
import pyrealsense2 as rs
import numpy as np
import functions.cameraparams
import os
import matplotlib

matplotlib.use('TkAgg')
from matplotlib import pyplot as plt


def funnyfun(funcz, argums, depth_load, keypoints, intr, keylist, truelist, truelistarray,
             combolist,namez):
    biglist = []
    dictlist = []

    for iterator in range(0, 51):
        point_dict = {}
        if 'bilateral' in namez:
            depth_load = np.float32(depth_load)
            # depth_load = np.uint8(depth_load)
        depth_load_filter = funcz(depth_load[iterator], *argums)

        testarrayX = keypoints[iterator][:, 0]
        testarrayY = keypoints[iterator][:, 1]

        # !!!!! IMPORTANT
        # ROW COLUMN =! X,Y
        # ROW COLUMN IS Y,X

        for x, y, key in zip(testarrayX, testarrayY, keylist):
            x = int(round(x))
            y = int(round(y))

            z = depth_load_filter[y, x]
            point_dict[key] = (x, y, z)

        distance_list = []
        dictlist.append(point_dict)

        for keys, truevalue in zip(combolist, truelist):
            item = [tuple, tuple]
            for key, it in zip(keys, [0, 1]):
                n = 0
                while dictlist[iterator - n][key][2] == 0:
                    n += 1
                item[it] = dictlist[iterator - n][key]

            point1 = rs.rs2_deproject_pixel_to_point(intr, item[0][0:2], item[0][2])
            point2 = rs.rs2_deproject_pixel_to_point(intr, item[1][0:2], item[1][2])
            mydist = functions.basics.eucli_dist(point1, point2) / 10
            distance_list.append(mydist)

        biglist.append(distance_list)

    # # # # # # # # #
    # END FOR LOOP
    # # # # # # # # #

    bias, sd = functions.basics.calc_sdb(biglist, truelistarray)

    # average bias and standard deviation
    return sum(bias) / len(bias), sum(sd) / len(sd)


def getparams(current_time):
    intr = functions.cameraparams.load_params(Windows=False)

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

    keypoints = []
    depth_load = []

    path_KP = "./data/" + current_time + "/Keypoints/"
    path_depth = "./data/" + current_time + "/Depth/"
    depth_filename = "dfile_"
    kp_filename = "kp_"

    for iterator in range(0, 135):
        path_keypoints = path_KP + kp_filename + repr(iterator) + ".txt"
        path_depthfile = path_depth + depth_filename + repr(iterator) + ".txt"

        # reading and correctly closing the json (containing keypoints)
        with open(path_keypoints) as file_kp:
            keypoints.append(np.loadtxt(file_kp))

        # same for the depth file
        with open(path_depthfile) as file_depth:
            # file_depth2 = str(file_depth)
            depth_load.append(np.loadtxt(file_depth))

    return depth_load, keypoints, intr, keylist, truelist, truelistarray, combolist


def get_plot(data, name, path):
    matplotlib.rcParams.update({'font.size': 21})
    plt.rcParams["figure.figsize"] = (11, 7.5)

    bias, std, cum_avg = data

    plt.plot(bias, linewidth=3, color='lightcoral')
    plt.plot(std, linewidth=3, color='#4b0082')
    plt.plot(cum_avg, linewidth=3, color='olive')

    plt.ylabel('some numbers')
    plt.xlabel('kernel size')
    plt.ylabel('value (cm)')
    plt.legend(['bias', 'std', 'cum_avg'])
    plt.title(f"{name} kernel")
    plt.savefig(f"{path}{name}.png")
    plt.close()


def save_results(the_path, data, name):
    path_r = f"./data/{the_path}/results/"
    if not os.path.exists(path_r):
        os.mkdir(path_r)

    path_w = f"./data/{the_path}/results/{name}/"
    if not os.path.exists(path_w):
        os.mkdir(path_w)

    sdata = sorted(data)
    bias = []
    std = []
    cum_avg = []

    print(sdata)

    for element in sdata:
        if element[1][0]:
            bias.append(element[1][0])
        if element[1][1]:
            std.append(element[1][1])
        if element[1][2]:
            cum_avg.append(element[1][2])

    bias = [item for sublist in bias for item in sublist]
    std = [item for sublist in std for item in sublist]
    cum_avg = [item for sublist in cum_avg for item in sublist]

    print(cum_avg)
    print(std)
    print(bias)

    np.savetxt(f"{path_w}bias.txt", bias)
    np.savetxt(f"{path_w}std.txt", std)
    np.savetxt(f"{path_w}cum_avg.txt", cum_avg)

    get_plot([bias, std, cum_avg], name, path_w)

    return [bias, std, cum_avg]
