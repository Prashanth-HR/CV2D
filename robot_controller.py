import math
import random
import socket
import time

from robot_receiver import Robot_Receiver
from robot_transmitter import Robot_Transmitter

transmitter =  Robot_Transmitter()
receiver = Robot_Receiver()

def main():
    tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    # Go to the Precalibrated position .1, .1, .1 and orientation .0, .0, pi.
    calibrated_position = [-600, -300, 600, -3*math.pi/4, .0, math.pi]
    # Command the robot to move to position .1, .1, .1 and orientation
    # (intrinsic ZYX Euler angles) .0, .0, pi.
    message = transmitter.generate_set_pose_abs_message(1, 50, 120, calibrated_position)
    tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))

    # Connect to camera and take a picture


    # Run obj_detection and 2D>3D conversion ,returns => an array(pos_3D) of detected 3D coordinates
    pos_3D = []

    for position in pos_3D:

        # For each detected point => move to the position  

        # Command the robot to move to position .1, .1, .1 and orientation
        # (intrinsic ZYX Euler angles) .0, .0, pi.
        message = transmitter.generate_set_pose_abs_message(1, 50, 120, position)
        tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))

        # => start the gripper suction
    

        # => Move to a diff position to release obj 


        # => go to pre-calibrated position 


        # => continue loop for next obj



    # Move to pre-calibrated position
    message = transmitter.generate_set_pose_abs_message(1, 50, 120, [.1, .1, .1, .0, .0, math.pi])
    tx_socket.sendto(message, (transmitter.IP_ADDR, transmitter.PORT))



if __name__ == "__main__":
    main()
