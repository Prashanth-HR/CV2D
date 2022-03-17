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

- Flase - $ pip install flask

## 2. Assuming that u have calibrated the camera by running the calibration scriprts in /cam_calibration

The code is in **test.py** file under ***main()*** method


## 3. To Run the algorithm as a service

- run $ python server.py



## NodeRed Interface flow
- import **flows.json** into the NodeRed interface to import the flow. If needed, one can change the url param in the http node to a diff value depending upon where u run server.py script. 

##### Object Detection Ref:
- https://github.com/pacogarcia3/hta0-horizontal-robot-arm/blob/master/README.md