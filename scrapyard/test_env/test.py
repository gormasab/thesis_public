import cv2
import matplotlib.pyplot as plt
import numpy as np
import pyrealsense2 as rs
import sys
from PIL import Image
import inspect

"""
sketch version of depth_J
"""

def scale_im(img):
    immax = np.max(img)
    temp = []
    for element in np.nditer(img):
        # temp.append(np.log((element/immax)+1))
        if element > 2000:
            temp.append(0)
        else:
            temp.append((element / 2000))

    image = np.reshape(temp, (480, 640))
    return image


def get_concat_v(im1, im2):
    print(im1.shape)
    print(im2.shape)
    width1, height1, channels = im1.shape
    width2, height2 = im2.shape
    dst = Image.new('RGB', (width1, height1 + height2))
    dst.paste(im1, (0, width1, height1,width1))
    dst.paste(im2, (height1, width1,2*height1,2*width1))
    return dst


pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
# different resolutions of color and depth streams
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))
print(device_product_line)
print(device)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: ", depth_scale)

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

while True:
    frames = pipeline.wait_for_frames()
    print("cycle")
    # Get aligned frames
    depth_frame = frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
    color_frame = frames.get_color_frame()

    depth_try = np.zeros((480, 640, 3))
    depth_image = np.asanyarray(depth_frame.get_data())  # get the array of depth
    depth_try[:, :, 0] = depth_image

    a = color_frame.get_data()
    color_image = np.asanyarray(color_frame.get_data())  # get the array of rgb
    color_image2 = np.asarray(color_frame.get_data())  # get the array of rgb
    width, height, channel = color_image2.shape

    #    color_image = np.asarray(color_image, dtype='uint16')

    r = color_image[:, :, 0]
    # r = np.zeros((480,640),dtype='uint8')
    # g = np.zeros((480,640),dtype='uint8')
    g = color_image[:, :, 1]
    b = color_image[:, :, 2]
    # b = np.zeros((480,640),dtype='uint8')

    color_image3 = np.dstack((b, g, r))

    print("stop")
    # color_image3 = np.reshape(color_image3,(480,640,3))

    depth_show = scale_im(depth_image)
    dd=get_concat_v(color_image2, depth_show)
    plt.imshow(dd)
    imgplot = plt.imshow(depth_show)


    plt.show()
    plt.pause(1 / 30)
    # plt.close()

pipeline.stop()

