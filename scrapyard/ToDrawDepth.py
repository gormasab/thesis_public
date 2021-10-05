#Reihaneh Shahmoradi

# First import the libraries
import pyrealsense2 as rs
import numpy as np
import cv2
from scipy import ndimage, misc
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import itertools
import matplotlib.pyplot as plt
from scipy.signal.signaltools import wiener
import scipy, matplotlib


"""
This function takes a depth image, shows it and creates a 3D plot. It also has the possibility of 
doing filters. 

- Median
- Gauss
- Wiener
- Bilateral

"""


# Create a pipeline
pipeline = rs.pipeline()

# Create a config 
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

#config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# Start streaming
profile = pipeline.start(config)
# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)


# Streaming loop
try:
    while True:
        # Get frameset of depth
        frames = pipeline.wait_for_frames()

        depth_frame = frames.get_depth_frame() 

        # Validate that both frames are valid
        if not depth_frame: #or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        #depth_image= open('/home/reyhun/asasi2/5.txt')
        #depth_image=np.loadtxt
        #without filter
        result=depth_image
            #median filter
        result = ndimage.median_filter(depth_image, size=15)
            #gaussian filter
        #result = gaussian_filter(depth_image, sigma=15)
            #wiener filter
        #result = wiener(depth_image, (15, 15))
            #bilateral filter
        #depth_image = np.uint8(depth_image)
        #result = cv2.bilateralFilter(depth_image, 15, 75, 75)
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(result, alpha=0.03), cv2.COLORMAP_JET)
    
        #makeing x y z
        x=[0]
        y=[0]
        z=[0]
        for i in range (1,result.shape[0],3):
            for j in range (1,result.shape[1],3):
             x.append(j)
             y.append(i)
             z.append(result[i,j])
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(x, y, z, c=z, cmap='viridis', linewidth=0.1)
        plt.show()                   

        cv2.imshow('Align Example', depth_colormap)
        #print (depth_image[3,11])
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            break
        
   
finally:
    pipeline.stop()