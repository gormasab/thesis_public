# Reihaneh Shahmoradi

import cv2
import numpy as np
import pyrealsense2 as rs

"""
live time video viewer of RGB stream camera
"""

# Initialize camera
pipeline = rs.pipeline()
config = rs.config()
# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

print(device, device_product_line)

# config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
profile = pipeline.start(config)

# Streaming loop
while True:
    # Get frameset of color
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()

    # if color_frame is None, loop back
    if not color_frame:
        continue

    # Everything coming out of the pipleline are highly specific 'pyrealsense.frame' objects.
    # however they support 'np.array' conversion.
    color_image = np.array(color_frame.get_data())
    cv2.imshow('RGB image', color_image)
    key = cv2.waitKey(1)

    # Press esc or 'q' to close the image window
    if key & 0xFF == ord('q') or key == 27:
        cv2.destroyAllWindows()
        break

pipeline.stop()
