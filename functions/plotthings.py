import pickle
import matplotlib
import numpy as np
from matplotlib import pyplot as plt

import os
try:
    from syscheck import iswindows as isw
except ModuleNotFoundError:
    from functions.syscheck import iswindows as isw
from matplotlib.pyplot import figure
matplotlib.use('TkAgg')

"""
Code is responsible for making the joint pair plot with standard deviation, measured value etc.
It takes: a distance list and bias/sd list.
This function can be ran standalone, then it will take a saved list. If called as a function
it should be provided as argument.

outputs plots. 
"""


def plotmaker(frames, sd, saveloc,combolist,truelist, special = "tsr"):
    """Frames is a list of lists...
    Each first list is a single frame. Each frame contains 12 distances. Distance is between
    joint pairs"""
    frames_length = len(frames)
    joint_pair_length = len(frames[0])

    """"Longlist removes the list of list structures and just puts them in one long list"""
    longlist = []

    for item in frames:
        for number in item:
            longlist.append(number)

    """sorted_joint_pairs is list containing 12 lists, and each inner list is of length
    frames_length."""

    sorted_joint_pairs = []
    for i in range(joint_pair_length):
        joint_pair = []
        for j in range(frames_length):
            # frame loop
            joint_pair.append(longlist[i + joint_pair_length * j])
        sorted_joint_pairs.append(joint_pair)

    for r in range(joint_pair_length):
        figure(figsize=(8, 6.5), dpi=80)
        matplotlib.rcParams.update({'font.size': 21})
        plt.rcParams["figure.figsize"] = (11, 7.5)
        data = sorted_joint_pairs[r]
        avg = sum(data) / len(data)
        i = range(0, frames_length, 1)

        true_value = np.zeros(frames_length) + truelist[r]
        avg = np.zeros(frames_length) + avg

        stand_dev_p = np.zeros(frames_length) + sd[r] + avg
        stand_dev_m = np.zeros(frames_length) - sd[r] + avg

        plt.title(f"{combolist[r][0]} + {combolist[r][1]}")
        plt.plot(i, data)
        plt.plot(i, true_value)
        plt.plot(i, avg, color='olive')
        plt.plot(i, stand_dev_m, linestyle='dashed', color='olive')
        plt.plot(i, stand_dev_p, linestyle='dashed', color='olive')

        plt.xlabel('Frame')
        plt.ylabel('Distance (cm)')
        # plt.legend(['Measured Value', 'True Value', 'Average', 'St. Dev. + ', 'St. Dev. - '])
        if os.path.exists(isw(saveloc)):
            plt.savefig(isw(f"{saveloc}/{special}_{r}.png"))
            plt.close()
        else:
            print(os.getcwd())


if __name__ == "__main__":
    import main
    file = open(isw('../scrapyard/distance_list.txt'), 'rb')
    frames = pickle.load(file)
    file.close()

    file = open(isw('../scrapyard/biasd.pcl'), 'rb')
    _, sd = pickle.load(file)
    file.close()

    saveloc = isw("../data/manual")

    plotmaker(frames, sd, saveloc)
