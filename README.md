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

## 2. Calibrate the camera and test the CV2D code locally
- [calibration docs](/cam_calibration/README.md)
    - run the scripts available under *./cam_calibration/* 

- [camera configurations](/config-a2A3840-13gmPRO_40137700.pfs)

- when the camera is successfully calibrated, the calibration data is stored under *./camera_data/*

- To capture images from the Basler camera, run *$ python camera_control.py*. The script uses the data in *config-a2A3840-13gmPRO_40137700.pfs*  as camera configurations.

- To test the object recognition
    - We need 2 images: image of the scene with no objects *i.e background image* and an image with objects in the scene *i.e sample image*.
    - change the background image param(*img_bg*) and sample image param(*img_example*) in the script to desired values.
    - run *$ python object_recognition.py* 

- Assuming that the camera is calibrated by running all the calibration scriprts, test the CV2D code by running *$ python test.py*.


## 3. To Run the algorithm as a service

- run *$ python server.py*


# NodeRed Integration
- import [flows.json](/flows.json) into the NodeRed interface. 
- open the imported flow named **CV2D**
- change the param in the http node to the url obtained from running *server.py* script. 


##### Resources 
- Object Detection Ref: https://github.com/pacogarcia3/hta0-horizontal-robot-arm/blob/master/README.md
- NodeRED 
    - graphical programming : https://docs.robco.de/sections/node_programming.html
    - test based programming : https://docs.robco.de/sections/text_based_programming.html

Additionally, We also tried different state of the art object detection and matching algorithms and the results are documented [here.](/code_attempts/README.md)