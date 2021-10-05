#####################################################
##              Align Depth to Color               ##
#####################################################

# Import Numpy for easy array manipulation
import numpy as np
# First import the library
import pyrealsense2 as rs
# import keyboard
from PIL import Image as im

# Import OpenCV for easy image rendering
# Create a pipeline
pipeline = rs.pipeline()

# Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: ", depth_scale)

# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
# clipping_distance_in_meters = 0.7 #1 meter
# clipping_distance = 0.7 / depth_scale

# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)
i = 0

# Streaming loop
try:

    while True:
        # Get frameset of color and depth
        i = i + 1
        frames = pipeline.wait_for_frames(45000)

        # Get aligned frames
        depth_frame = frames.get_depth_frame()  # aligned_depth_frame is a 640x480 depth image
        color_frame = frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())  # get the array of depth
        color_image = np.asanyarray(color_frame.get_data())  # get the array of rgb

        image_rgb = im.fromarray(color_image)

        savestr = r'C:\Users\rey\Desktop\asasi7\ax' + str(i) + '.png'
        image_rgb.save(savestr)

        savedepth = r'C:\Users\rey\Desktop\asasi8\ax' + str(i) + '.txt'
        np.savetxt(savedepth, depth_image)

        # if keyboard.is_pressed('q'):
        # break


finally:

    pipeline.stop()
