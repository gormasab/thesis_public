# Reihaneh Shahmoradi

import pyrealsense2 as rs
import pickle

try:
    from syscheck import iswindows as isw
except ModuleNotFoundError:
    from functions.syscheck import iswindows as isw
""""
Functions used to save/load/check camera parameters.
"""


def save_parameters(path):
    # Initialize camera
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    profile: rs.pipeline_profile = pipeline.start(config)
    profile2 = profile.get_stream(rs.stream.depth)
    intr: rs.intrinsics = profile2.as_video_stream_profile().get_intrinsics()

    mylist = [intr.width, intr.height, intr.ppx, intr.ppy,
              intr.fx, intr.fy, intr.model, intr.coeffs]

    pipeline.stop()
    file = open(path, 'wb')
    pickle.dump(mylist, file)
    file.close()


def load_params():
    path = isw("./functions/camera_parameters.jb")
    file = open(path, 'rb')
    mylist = pickle.load(file)

    # depends on how it is saved. works for this configuration
    c_intr = rs.intrinsics()
    c_intr.width = mylist[0]
    c_intr.height = mylist[1]
    c_intr.ppx = mylist[2]
    c_intr.ppy = mylist[3]
    c_intr.fx = mylist[4]
    c_intr.fy = mylist[5]
    c_intr.model = mylist[6]
    c_intr.coeffs = mylist[7]

    return c_intr


def sanity_check(intr1):
    # given camera parameters, check if they match with previously gotten results

    # these should be the results
    R_ankle_X = 19927.568359375
    R_ankle_Y = 50319.15625
    R_ankle_Z = 65536.0

    # input data
    R_ankle_x = 204
    R_ankle_y = 534
    R_ankle_z = 65536
    resultA = [R_ankle_X, R_ankle_Y, R_ankle_Z]
    resultB = rs.rs2_deproject_pixel_to_point(intr1, [R_ankle_x, R_ankle_y], R_ankle_z)

    print(f"result A={resultA}, result B={resultB}")
    print(f"are they equal? {resultA == resultB}")
