# rec-bagfile-realsense
Recording of bag files using RealSense(D435i) at Intel corporation and image conversion.

## Features
This program records 3D information using RealSense. The program for image acquisition records information in bag format; the program for outputting information from bagfile can be used to output information saved in bag format as an image or csv.

## Requirement
pyrealsense : https://pypi.org/project/pyrealsense/
seaborn : https://pypi.org/project/seaborn/

## Usage
### About the program (Capture_bagfile.py) for image acquisition
saved_dir is the directory where you want to save bagfile.  
The duration time should be entered as an integer.  
```bash
python Capture_bagfile.py $saved_directory $duration_time
```
### About image export program from bagfile
saved_dir is the directory where you want to save image file.  
target_dir is the directory where bagfile is located.
```bash
python Restoration_bagfile.py $target_dir $saved_directory
```

## Note
I don't test environments under Mac.  
**Note that bagfile can be very large in file size.**

We hope you enjoy your life using RealSense!   
Thank you!