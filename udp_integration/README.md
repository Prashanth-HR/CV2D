# This is the code to communicate with the robot via UDP messages for CV2D.

## robot_receiver.py
It has the template code to parse UDP messages sent back from the robot so that it can be used in our code. It can be used to
- check if the robot is connected.
- get the robot's absolute position.


## robot_transmitter.py
It has the code to generate UDP messages to be sent to the robot in a format that the robot can parse the message sent. It can be used to
- move the robot to a desired position by the position coordinate and orientation.
- move the robot to a position using the robot joint angles.
- stop the robot in case of any emergencies
- set the output to true or false. (It can be used to control externat devices like compressed air cylinder connected to the robot)


## robot_controller.py
It is the file that integrates Basler camera configuration, object recognition, 2d to 3d conversion.
When the script is started, the camera captures the image of the scene. The image is then used by the object recognition algorithm to detect any objects and generate the center pixel coordinates of the object. This pixel coordinate is converted into the 3d coordinate.
For each 3d point, the script triggers a set of robot actions vis UDP messages.
- It moved the robot end of arm to that 3d point
- It starts the suction by setting the  output value to true for switch 0
- It moves the robot to dropping location
- It releases the suction to drop the object.
- It moves back to the pre calibrated position .. continues to the next object.


# The UDP comminication is not fully tested..  