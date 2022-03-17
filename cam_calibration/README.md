## Camera calibration:

### 1. initial_camera_calibration
- it is used to calibrate the camera from a set of chess board images. 
- use camera calibration [pattern](./pattern/chessboard.png)
- chessboard images must be more than ten images taken from different orientations distances.
- saves the camera data in ../camera_data
- for more information follow the instructions under: https://docs.opencv.org/3.3.0/dc/dbb/tutorial_py_calibration.html

### 2. initial_perspective_calibration.py
- it is used to calibrate the presepective projection on the camera setting including the depth to the object plane.
- use perspective calibration [pattern](./pattern/perspective_pattern.pdf)
- during the prespective calibration, if any pixel coordinate is needed, one can run *cvImage.py* and get the desired pixel coordinate.
- for more information follow the instructions under: https://docs.opencv.org/3.3.0/dc/dbb/tutorial_py_calibration.html

### 3. camera_toXYZ.py
- once the camera is calibrated and the perspective_projection is calibrated as well:
  - We have an estimate of the depth to the object place
  - have access to all the ./camera_data created from the calibration scripts.
- use the above calculated data to convert a pixel cooudinate (u,v) to a 3D real world co-coordinate (X,Y,Z)