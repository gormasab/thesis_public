# Reihaneh Shahmoradi

import cv2
import numpy as np
import pyrealsense2
import pyrealsense2 as rs

from scrapyard.fake_openpose import testOpenpose

"""
live time video viewer of RGB stream camera + depth camera, used for testing and saving images. 
"""

# parameters
fps = 30  # not any aribitrary number works! so far [30]
maxdepth = 4000
empty_im = np.zeros((480, 640, 3)).astype('uint16')

# Initialize camera
pipeline = rs.pipeline()
config = rs.config()
# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

print(device, device_product_line)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, fps)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, fps)



# Start streaming
profile: rs.pipeline_profile = pipeline.start(config)
print(f"profile type is:{type(profile)}")
profile2 = profile.get_stream(rs.stream.depth)
intr: pyrealsense2.intrinsics = profile2.as_video_stream_profile().get_intrinsics()
print(intr)
# Streaming loop
while True:

    # Get frameset of color & depth
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    # Everything coming out of the pipleline are highly specific 'pyrealsense.frame' objects.
    # however they support 'np.array' conversion.
    color_image = np.array(color_frame.get_data())
    #joint_coords = testOpenpose.joint_coordinate(color_image)
    #color_image_drawn = testOpenpose.openposeImage(joint_coords, color_image)
    # color_image_drawn = color_image_drawn.astype('uint16')
    # color_image_drawn *= 256
    #
    # depth_image = np.array(depth_frame.get_data())
    # # truncate the extreme outliers. Specific to situation
    # depth_image = scale_im(depth_image, maxdepth)
    # # depth image requires some work-around
    # depth_image_large = np.copy(empty_im)
    # depth_image_large[:, :, 0] = depth_image
    #
    # stack_im = np.hstack((depth_image_large, color_image_drawn))
    #
    # cv2.imshow('RGB + Depth Stack', stack_im)
    cv2.imshow("test", color_image)
    key = cv2.waitKey(1)

    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break




dpt_frame = pipeline.wait_for_frames().get_depth_frame().as_depth_frame()
pixel_distance_in_meters = dpt_frame.get_distance(2,2)
print(pixel_distance_in_meters)
pipeline.stop()