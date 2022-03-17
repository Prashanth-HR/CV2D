## Camera calibration:

### 1. initial_camera_calibration
- it is used to calibrate the camera from a set of chess board images. 
- use camera calibration [pattern](./pattern/chessboard.png)
- chessboard images must be more than ten images taken from different orientations.
- saves the camera calibration data in ../camera_data
- for more information follow the instructions under: https://docs.opencv.org/3.3.0/dc/dbb/tutorial_py_calibration.html

### 2. initial_perspective_calibration.py
- it is used to calibrate the presepective projection on the camera setting including the depth to the object plane.
- use perspective calibration [pattern](./pattern/perspective_pattern.pdf)
- during the prespective calibration, if any pixel coordinate is needed, run *$ python cvImage.py* and get the desired pixel coordinate.
- for more information follow the instructions under: https://www.fdxlabs.com/calculate-x-y-z-real-world-coordinates-from-a-single-camera-using-opencv/

### 3. camera_toXYZ.py
- once the camera and the perspective_projection are calibrated:
  - We have an estimate of the depth from the camera to the object plane
  - have access to all the ./camera_data generated from the calibration scripts.
- use the above calculated data to convert a pixel cooudinate (u,v) to a 3D real world co-coordinate (X,Y,Z)