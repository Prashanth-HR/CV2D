## Camera calibration:

### 1. initial_camera_calibration
- it is used to calibrate the camera from a set of chess board images taked from the camera to be calibrated..


### 2. initial_perspective_calibration.py
- it is used to calibrate the presepective projection on the camera setting including the depth to the object plane..

### 3. camera_toXYZ.py
- once the camera is calibrated and the perspective_projection is calibrated as well.. We have an estimate of the depth to the object place na d have access to all the ./camera_data created from the calibration scripts..
- use the above calculated data to convert a pixel cooudinate (u,v) to a 3D real world co-coordinate (X,Y,Z)