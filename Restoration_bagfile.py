# coding:utf-8
import pyrealsense2 as rs
import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import cv2
import shutil
import time
import seaborn as sns
import sys

width = 1280
height = 720
framerate = 30

target_dir = sys.argv[1]
saved_dir = sys.argv[2]

def Save_data(filename):
    target_file_saved_dir = '{}{}/'.format(saved_dir, filename.split("/")[-1].split(".")[0])
    if(os.path.isdir(target_file_saved_dir) == True):
        shutil.rmtree(target_file_saved_dir)
    os.mkdir(target_file_saved_dir)
    # Configure depth and color streams
    config = rs.config()
    config.enable_device_from_file(filename, repeat_playback=False)
    config.enable_stream(rs.stream.infrared, 1, width, height, rs.format.y8, framerate)
    config.enable_stream(rs.stream.infrared, 2, width, height, rs.format.y8, framerate)
    config.enable_stream(rs.stream.depth, width, height, rs.format.z16, framerate)
    config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, framerate)

    count = 0
    # Start streaming
    pipeline = rs.pipeline()
    profile = pipeline.start(config)

    start = time.time()
    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            flag,frames = pipeline.try_wait_for_frames()
            if flag == False: break
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            ir1_frame = frames.get_infrared_frame(1)
            ir2_frame = frames.get_infrared_frame(2)
            if not depth_frame or not color_frame or not ir1_frame or not ir2_frame:
                continue

            depth_map = np.zeros((height,width))
            for w in range(width):
                for h in range(height):
                    dist = depth_frame.get_distance(w,h)
                    depth_map[h,w] = dist
            np.savetxt('{}Depth_map_{}.csv'.format(target_file_saved_dir,count), depth_map, delimiter=',', fmt='%.3f')
            fig, ax = plt.subplots()
            ax = sns.heatmap(depth_map)
            ax.set_aspect('equal')
            fig.savefig('{}Depth_map_color_{}.png'.format(target_file_saved_dir,count))

            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            ir1_image = np.asanyarray(ir1_frame.get_data())
            ir2_image = np.asanyarray(ir2_frame.get_data())
            
            depth_color_image = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.08), cv2.COLORMAP_JET)       
            
            # Show images
            cv2.imwrite("{}Depth_{}.png".format(target_file_saved_dir,count), depth_image)
            cv2.imwrite("{}Color_{}.png".format(target_file_saved_dir,count), color_image)
            cv2.imwrite("{}IR_Left_{}.png".format(target_file_saved_dir,count), ir1_image)
            cv2.imwrite("{}IR_Right_{}.png".format(target_file_saved_dir,count), ir2_image)
            cv2.imwrite("{}Depth_Color_{}.png".format(target_file_saved_dir,count), depth_color_image)
            count += 1
    finally:
        # Stop streaming
        pipeline.stop()

filenames = glob.glob('{}*.bag'.format(target_dir))
for filename in filenames:
    filename = filename.replace("\\","/")
    print(filename)
    Save_data(filename)