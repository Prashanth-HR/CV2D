import math
import random
import socket
import time



_tx_sequence_number = random.randint(0, 255)

class Robot_Transmitter:

    def __init__(self) -> None:
        self.IP_ADDR = "192.168.1.1"
        self.PORT = 25000
        self.MAX_MSG_LENGTH = 508
        self.MIN_MSG_LENGTH = 4


    def main(self):
        tx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        orientation = [-3*math.pi/4, .0, math.pi]
        calibrated_position = [-700, -300, 600, *orientation]
        message = self.generate_set_pose_abs_message(2, 50, 120, calibrated_position)
        tx_socket.sendto(message, (self.IP_ADDR, self.PORT))





    def generate_set_joint_abs_message(self, point_sequence_number, approach_velocity,
                                    approach_acceleration, joint_angles):
        message = bytes()
        message_type = 0x01  # SET_JOINT_ABS.
        message += message_type.to_bytes(1, byteorder='big', signed=False)
        message += self.get_message_sequence_number().to_bytes(1, byteorder='big',
                                                    signed=False)
        payload_length = 5 + (len(joint_angles) * 4)
        message += payload_length.to_bytes(2, byteorder='big', signed=False)
        message += point_sequence_number.to_bytes(1, byteorder='big', signed=False)
        approach_mode = 0x01  # Point-to-point.
        message += approach_mode.to_bytes(1, byteorder='big', signed=False)
        message += approach_velocity.to_bytes(1, byteorder='big', signed=False)
        message += approach_acceleration.to_bytes(1, byteorder='big', signed=False)
        number_of_joints = len(joint_angles)
        message += number_of_joints.to_bytes(1, byteorder='big', signed=False)
        for joint_angle in joint_angles:
            encoded_joint_angle = self.encode_angular_value(joint_angle)
            message += encoded_joint_angle.to_bytes(4, byteorder='big', signed=True)
        return message


    def generate_set_joint_offs_message(self, joint_offsets):
        message = bytes()
        message_type = 0x03  # SET_JOINT_OFFS.
        message += message_type.to_bytes(1, byteorder='big', signed=False)
        message += self.get_message_sequence_number().to_bytes(1, byteorder='big',
                                                    signed=False)
        payload_length = 1 + (len(joint_offsets) * 4)
        message += payload_length.to_bytes(2, byteorder='big', signed=False)
        number_of_joints = len(joint_offsets)
        message += number_of_joints.to_bytes(1, byteorder='big', signed=False)
        for joint_offset in joint_offsets:
            encoded_joint_offset = self.encode_angular_value(joint_offset)
            message += encoded_joint_offset.to_bytes(4, byteorder='big', signed=True
                                                    )
        return message


    def generate_set_pose_abs_message(self, point_sequence_number, approach_velocity,
                                    approach_acceleration, pose):
        message = bytes()
        message_type = 0x05  # SET_POSE_ABS.
        message += message_type.to_bytes(1, byteorder='big', signed=False)
        message += self.get_message_sequence_number().to_bytes(1, byteorder='big',
                                                    signed=False)
        payload_length = 5 + (len(pose) * 4)
        message += payload_length.to_bytes(2, byteorder='big', signed=False)
        message += point_sequence_number.to_bytes(1, byteorder='big', signed=False)
        approach_mode = 0x02  # Linear.
        message += approach_mode.to_bytes(1, byteorder='big', signed=False)
        message += approach_velocity.to_bytes(1, byteorder='big', signed=False)
        message += approach_acceleration.to_bytes(1, byteorder='big', signed=False)
        number_of_dimensions = len(pose)
        message += number_of_dimensions.to_bytes(1, byteorder='big', signed=False)
        for dimension_index in range(number_of_dimensions):
            if dimension_index < 3:
                encoded_position = self.encode_linear_value(pose[dimension_index])
                message += encoded_position.to_bytes(4, byteorder='big', signed=True
                                                    )
            else:
                encoded_position = self.encode_angular_value(pose[dimension_index])
                message += encoded_position.to_bytes(4, byteorder='big', signed=True
                                                    )
        return message


    def generate_set_output_message(self, index, value):
        message = bytes()
        message_type = 0x20  # SET_OUTPUT.
        message += message_type.to_bytes(1, byteorder='big', signed=False)
        message += self.get_message_sequence_number().to_bytes(1, byteorder='big',
                                                    signed=False)
        payload_length = 4 + 4
        message += payload_length.to_bytes(2, byteorder='big', signed=False)
        message += index.to_bytes(4, byteorder='big', signed=False)
        message += int(value).to_bytes(4, byteorder='big', signed=False)
        return message


    def generate_set_g_compensation_message(self):
        message = bytes()
        message_type = 0x41  # SET_G_COMPENSATION.
        message += message_type.to_bytes(1, byteorder='big', signed=False)
        message += self.get_message_sequence_number().to_bytes(1, byteorder='big',
                                                    signed=False)
        payload_length = 1
        message += payload_length.to_bytes(2, byteorder='big', signed=False)
        mode = 0  # Fully compensated but respecting joint limits.
        message += mode.to_bytes(1, byteorder='big', signed=False)
        return message


    def generate_set_stop_message(self):
        message = bytes()
        message_type = 0xEE  # SET_STOP.
        message += message_type.to_bytes(1, byteorder='big', signed=False)
        message += self.get_message_sequence_number().to_bytes(1, byteorder='big',
                                                    signed=False)
        payload_length = 1
        message += payload_length.to_bytes(2, byteorder='big', signed=False)
        rfu = 0  # Spacer. Reserved for future usage.
        message += rfu.to_bytes(1, byteorder='big', signed=False)
        return message


    def encode_angular_value(self, angular_value):
        # Angular values are encoded as nano radians divided by pi.
        return int(angular_value / math.pi * 1e9)


    def encode_linear_value(self, angular_value):
        # Linear values are encoded as micro meters.
        return int(angular_value * 1e6)


    def get_message_sequence_number(self):
        global _tx_sequence_number
        if _tx_sequence_number >= 0xff:
            _tx_sequence_number = 0x00
        else:
            _tx_sequence_number += 1
        return _tx_sequence_number