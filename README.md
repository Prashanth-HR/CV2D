# Modular Robotics - CV2D
Building a Modular Robot

- Develop a robust detection and localization solution based on supplied demo parts
- Develop a web-based interface that integrates into the robot's existing UI
- Include Mapping from camera to robot coordinates

# Steps to startup
## 1. Dependencies
- Recommended to work with Anaconda - manages the env's better
    - ref : https://docs.anaconda.com/anaconda/install/index.html

- OpenCV - $ sudo apt-get install python3-opencv
    - ref : https://docs.opencv.org/4.x/d2/de6/tutorial_py_setup_in_ubuntu.html

- Flask - $ pip install flask

## 2. Calibration and testing
- [docs](/cam_calibration/README.md) run the scripts available under *./cam_calibration/* 
- [camera config](/config-a2A3840-13gmPRO_40137700.pfs)
- when the camera is successfully calibrated, the calibration data is stored under *./camera_data/*
- To capture images from the Basler camera, run *$ python camera_control.py*. The script used *config-a2A3840-13gmPRO_40137700.pfs* for camera configurations.
- To test the object recognition locally, run *$ python object_recognition.py* 
    - change the background image param(*img_bg*) and sample image param(*img_example*) in the script to desired values.
- Assuming that the camera calibrated by running all the calibration scriprts, test the CV2D code by running *$ python test.py*.


## 3. To Run the algorithm as a service

- run *$ python server.py*


## NodeRed Integration
- import [flows.json](/flows.json) into the NodeRed interface. 
- change the url param in the http node to the url obtained from running *server.py* script. 


##### Resources 
- Object Detection Ref: https://github.com/pacogarcia3/hta0-horizontal-robot-arm/blob/master/README.md
- NodeRED 
    - graphical programming : https://docs.robco.de/sections/node_programming.html
    - test based programming : https://docs.robco.de/sections/text_based_programming.html
