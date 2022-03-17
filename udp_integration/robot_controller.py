import math
import socket

import cv2 as cv
import numpy as np
from cam_calibration.camera_toXYZ import camera_realtimeXYZ
from camera_control import Camera
from object_recognition import ObjectRecognition

from robot_receiver import Robot_Receiver
from robot_transmitter import Robot_Transmitter

transmitter =  Robot_Transmitter()
receiver = Robot_Receiver()
cameraXYZ = camera_realtimeXYZ()
obj_recognition = ObjectRecognition()
camera = Camera()


def main():
    tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # Go to the Precalibrated position .1, .1, .1 and orientation .0, .0, pi.
    orientation = [-3*math.pi/4, .0, math.pi]
    calibrated_position = [-600, -300, 600, *orientation]
    release_obj_pos = [-600, -300, 70, *orientation]

    # calibrated_position = [-600, -300, 600, -135, 0, 180]

    # Command the robot to move to position .1, .1, .1 and orientation
    # (intrinsic ZYX Euler angles) .0, .0, pi.
    message = transmitter.generate_set_pose_abs_message(1, 50, 120, calibrated_position)
    tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))

    # Connect to camera and take a picture
    # img = cv.imread('images/test_images/multi-obj1.bmp')
    img = camera.get_image()
    img_bg = cv.imread('images/background.bmp')

    # Run obj_detection and 2D>3D conversion ,returns => an array(pos_3D) of detected 3D coordinates
    # Get pixel centers of the detected objs
    cordPixels = obj_recognition.obj_recognize(img, img_bg)
    
    # Convert the pixel centers to 3D cords
    cord3D = [cameraXYZ.calculate_XYZ(*cord2D) for cord2D in cordPixels]
    cord3D = np.squeeze(cord3D)
    for position in cord3D:

        # for constant Z value
        position[2] = 70
        # append the orientation
        message = transmitter.generate_set_pose_abs_message(1, 50, 120, [*position, *orientation])
        tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))

        # => start the gripper suction
        message = transmitter.generate_set_output_message(0, True)
        tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))

        # => Move to a diff position to release obj 
        message = transmitter.generate_set_pose_abs_message(1, 50, 120, release_obj_pos)
        tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))

        # => start the gripper suction
        message = transmitter.generate_set_output_message(0, False)
        tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))

        # => go to pre-calibrated position 
        message = transmitter.generate_set_pose_abs_message(1, 50, 120, calibrated_position)
        tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))

        # => continue loop for next obj



    # Move to pre-calibrated position
    message = transmitter.generate_set_pose_abs_message(1, 50, 120, calibrated_position)
    tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))



if __name__ == "__main__":
    main()
