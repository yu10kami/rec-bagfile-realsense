# coding:utf-8
import pyrealsense2 as rs
import numpy as np
import time
from datetime import datetime
import sys

width = 1280
height = 720
framerate = 30

saved_dir = sys.argv[1]
dt_start = str(datetime.now().strftime('%Y%m%d%H%M%S'))

# Configure depth and color streams
config = rs.config()
config.enable_stream(rs.stream.infrared, 1, width, height, rs.format.y8, framerate)
config.enable_stream(rs.stream.infrared, 2, width, height, rs.format.y8, framerate)
config.enable_stream(rs.stream.depth, width, height, rs.format.z16, framerate)
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, framerate)
config.enable_record_to_file('{}{}.bag'.format(saved_dir, dt_start))
# Start streaming
pipeline = rs.pipeline()
pipeline.start(config)

start = time.time()
frame_no = 1
duration_time = int(sys.argv[2]) # [second (60th min)]
try:
    while time.time() - start <= duration_time:
        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        ir1_frame = frames.get_infrared_frame(1)
        ir2_frame = frames.get_infrared_frame(2)
        fps  = frame_no / (time.time() - start)  
        print(fps)
        frame_no = frame_no+1  
        if not ir1_frame or not ir2_frame or not color_frame:   
            ir1_image = np.asanyarray(ir1_frame.get_data())
            ir2_image = np.asanyarray(ir2_frame.get_data())   
            color_image = np.asanyarray(color_frame.get_data())

finally:    
    pipeline.stop()