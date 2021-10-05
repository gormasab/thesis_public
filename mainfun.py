# Reihaneh Shahmoradi
import cv2
import numpy as np
from scipy import ndimage

from functions.parallel import funnyfun as funnyfun
from functions.parallel import getparams as getparams
from functions.parallel import save_results as save_results
from multiprocessing import Process
from multiprocessing import Queue
from scipy.signal import wiener


def multi_funnyfun(original_args, listo, q: Queue, count, fun, argu, namez):
    """"called by each process to calculate std/bias"""
    bias = []
    std = []
    cum_avg = []

    depth_load, keypoints, intr, keylist, truelist, truelistarray, combolist = original_args
    a, b = listo
    for ii in range(a, b + 1):

        if 'bilateral' in namez:
            print("hit")
            inp = [argu, ii, ii]
        else:
            inp = [ii]
        bias_r, std_r = funnyfun(fun, inp, depth_load, keypoints, intr, keylist,
                                 truelist, truelistarray, combolist, namez)
        cum_avg_r = np.sqrt(bias_r ** 2 + std_r ** 2)
        bias.append(bias_r)
        std.append(std_r)
        cum_avg.append(cum_avg_r)
        print(ii)

    queobj = [count, [bias, std, cum_avg]]
    q.put(queobj)

    print(f"Process {count} finished!")


def getcut(cores, order, max):
    n = np.arange(0, cores + 1)
    xp = ((n / cores) ** (1 / (order + 1))) * (max - 1) + 1
    xp = np.round(xp)

    thecut = []

    for cut in range(cores):
        if not thecut:
            thecut.append([int(xp[cut]), int(xp[cut + 1])])
        else:
            thecut.append([int(xp[cut] + 1), int(xp[cut + 1])])

    return thecut


# # #########################################################################
procs = 8
maxsize = 250
current_time = "20_20_28"
all_params = getparams(current_time)  # loads in all the keypoints & depth values & other stuff

filters = []
# filters.append([ndimage.median_filter, 'median', None])
filters.append([ndimage.gaussian_filter, 'gaussian', None])
# filters.append([wiener,'wiener',None])
# filters.append([cv2.bilateralFilter,'bilateral1',1])
# filters.append([cv2.bilateralFilter,'bilateral2',2])
# filters.append([cv2.bilateralFilter,'bilateral3',3])
# filters.append([cv2.bilateralFilter,'bilateral4',4])
# filters.append([cv2.bilateralFilter, 'bilateral5', 5])

for filter in filters:
    func = filter[0]
    name = filter[1]
    argz = filter[2]

    thecut = getcut(procs, 2, maxsize)
    q = Queue()
    data = []
    processes = []

    for element in range(procs):

        processes.append(Process(target=multi_funnyfun,
                                 args=(all_params, thecut[element], q, element, func,
                                       argz, name)))
        processes[element].start()

    for element in processes:
        element.join()

    while not q.empty():
        data.append(q.get())

    vals = save_results(current_time, data, name)
