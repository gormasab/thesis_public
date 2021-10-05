import pyrealsense2 as rs
import numpy as np
import cv2
import os
import functions.basics
from datetime import datetime
import argparse
import sys

now = datetime.now()
current_time = now.strftime("%H_%M_%S")
RGB_filename = "RGB_"
depth_filename = "dfile_"
keypoint_filename = "kp_"

savetings = True  # set false to NOT write to disk
Windows = False  # OS == Windows? Should automate this task
displayed = True
process_img = True

if process_img:
    try:
        sys.path.append('/usr/local/python')  # used to import openpose
        from openpose import pyopenpose as op

    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON'
              ' in CMake and have this Python script in the right folder?')
        raise e

    params = dict()
    params["model_folder"] = "/home/rey/Downloads/openpose/models"

    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
    datum = op.Datum()

if Windows is True:
    path_depth = ".\\data\\" + current_time + "\\Depth\\"
    path_RGB = ".\\data\\" + current_time + "\\RGB\\"
    path_KP = ".\\data\\" + current_time + "\\Keypoints\\"
else:
    path_KP = "./data/" + current_time + "/Keypoints/"
    path_depth = "./data/" + current_time + "/Depth/"
    path_RGB = "./data/" + current_time + "/RGB/"

if savetings:
    if Windows is True:
        functions.basics.create_folder(".\\data\\" + current_time)
    else:
        functions.basics.create_folder("./data/" + current_time)
    print(f"Folders created under current time: {current_time}")

# Create a pipeline
pipeline = rs.pipeline()
config = rs.config()
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()

clipping_distance_in_meters = 3
clipping_distance = clipping_distance_in_meters / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

# Streaming loop
iterator = 0

try:
    while True:
        frames = pipeline.wait_for_frames()  # Get frameset of color and depth
        aligned_frames = align.process(frames)  # Align the depth frame to color frame

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue  # goto top of the loop

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        if savetings:
            cv2.imwrite(path_RGB + RGB_filename + str(iterator) + ".png", color_image)
            cv2.imwrite(path_depth + depth_filename + str(iterator) + ".png", depth_image)
            np.savetxt(path_depth + depth_filename + str(iterator) + ".txt", depth_image)


        if process_img:
            datum.cvInputData = color_image
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            processed_img = datum.cvOutputData
            keypoints = datum.poseKeypoints
            if savetings & (keypoints is not None):
                np.savetxt(path_KP+keypoint_filename+str(iterator)+".txt", keypoints[0])

        if displayed:
            if not process_img:
                # Remove background - Set pixels further than clipping_distance to grey
                depth_image_3d = np.dstack((depth_image, depth_image, depth_image))
                bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), (153, 153, 153),
                                      color_image)
                bg_removed2 = bg_removed.astype('uint8')
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.1), cv2.COLORMAP_JET)
                images = np.hstack((bg_removed2, depth_colormap))

                cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
                cv2.imshow('Align Example', images)
            else:
                cv2.namedWindow('OpenPose fun!', cv2.WINDOW_NORMAL)
                cv2.imshow('It Works!', processed_img)

            iterator += 1
            key = cv2.waitKey(1)
            # Press esc or 'q' to close the image window
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break

finally:
    pipeline.stop()
