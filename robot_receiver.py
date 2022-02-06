import math
import socket
import this



_last_rx_mesage_sequence_number = 0x00

class Robot_Receiver:

    def __init__(self) -> None:
        self.IP_ADDR = "192.168.1.2"
        self.PORT = 25001
        self.MAX_MSG_LENGTH = 508
        self.MIN_MSG_LENGTH = 4

    def main():
        rx_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        rx_socket.bind((self.IP_ADDR, self.PORT))
        while True:
            data, address = rx_socket.recvfrom(self.MAX_MSG_LENGTH)
            if len(data) > 0:
                success = self.process_message(data)
                if not success:
                    print("Error decoding message.")


    def process_message(message):
        global _last_rx_mesage_sequence_number
        success = False
        if(len(message) >= self.MIN_MSG_LENGTH) and (len(message) <= self.MAX_MSG_LENGTH):
            # Valid message size verified. Continue processing.
            message_type = int.from_bytes(message[0:1], byteorder='big',
                                        signed=False)
            message_sequence_number = int.from_bytes(message[1:2], byteorder='big',
                                                    signed=False)
            if message_sequence_number == _last_rx_mesage_sequence_number:
                print("Duplicate message detected.")
            _last_rx_mesage_sequence_number = message_sequence_number
            payload_length = int.from_bytes(message[2:4], byteorder='big',
                                            signed=False)
            payload = message[4:]
            if payload_length == len(payload):
                if message_type == 0x02:  # GET_JOINT_ABS.
                    success = self.process_get_joint_abs_payload(payload)
                elif message_type == 0x06:  # GET_POSE_ABS.
                    success = self.process_get_pose_abs_payload(payload)
                elif message_type == 0x11:  # GET_MOTION_DONE. # Deprecated.
                    success = self.process_get_motion_done_payload(payload)
                elif message_type == 0x21:  # GET_INPUT.
                    success = self.process_get_input_payload(payload)
                elif message_type == 0x23:  # GET_OUTPUT.
                    success = self.process_get_output_payload(payload) 
                elif message_type == 0x50:  # GET_STATUS.
                    success = self.process_get_status_payload(payload)
                else:
                    print("Unhandled message type received.")
            else:
                print("Payload length does not match expected value.")
        return success


    def process_get_joint_abs_payload(payload):
        success = False
        joint_values = []
        number_of_joints = int.from_bytes(payload[0:1], byteorder='big',
                                        signed=False)
        # Each joint value is 4 Bytes long.
        if number_of_joints == (len(payload[1:]) / 4):
            for joint_index in range(number_of_joints):
                # Iterate over 32 Bit integers: 4 Bytes per encoded value, 1 byte
                # offset to first payload Byte.
                raw_joint_value = int.from_bytes(payload[((joint_index * 4) + 1):((
                        (joint_index + 1) * 4) + 1)], byteorder='big', signed=True)
                joint_values.append(self.decode_angular_value(raw_joint_value))
            print("Joint values: ", joint_values)
            success = True
        return success


    def process_get_pose_abs_payload(payload):
        success = False
        pose_values = []
        number_of_dimensions = int.from_bytes(payload[0:1], byteorder='big',
                                            signed=False)
        # Each dimensional value is 4 Bytes long.
        if (number_of_dimensions == (len(payload[1:]) / 4)) and \
                (number_of_dimensions == 6):
            for dimension_index in range(number_of_dimensions):
                # Iterate over 32 Bit integers: 4 Bytes per encoded value, 1 Byte
                # offset to first payload Byte.
                raw_dimensional_value = int.from_bytes(
                    payload[((dimension_index * 4) + 1):(((dimension_index + 1) * 4)
                                                        + 1)], byteorder='big',
                    signed=True)
                if dimension_index < 3:  # Linear position values.
                    pose_values.append(self.decode_linear_value(raw_dimensional_value))
                else:  # Angular orientation values (ZYX Euler intrinsic).
                    pose_values.append(self.decode_angular_value(raw_dimensional_value))
            print("Pose values: ", pose_values)
            success = True
        return success


    def process_get_motion_done_payload(payload):
        success = False
        if len(payload) == 1:  # Expected payload length: 1 Byte.
            point_sequence_number = int.from_bytes(payload[0:1], byteorder='big',
                                                signed=False)
            print("Reached waypoint. Id: ", point_sequence_number)
            success = True
        return success


    def process_get_input_payload(payload):
        success = False
        input_values = []
        number_of_values = int.from_bytes(payload[0:1], byteorder='big',
                                        signed=False)
        # Each input value is 4 Bytes long.
        if number_of_values == (len(payload[1:]) / 4):
            # Iterate over 32 Bit integers: 4 Bytes per encoded value, 1 byte
            # offset to first payload Byte.
            for value_index in range(number_of_values):
                input_values.append(int.from_bytes(payload[((value_index * 4) + 1):(
                        ((value_index + 1) * 4) + 1)], byteorder='big', signed=False
                        ))
            print("Input values: ", input_values)
            success = True
        return success


    def process_get_output_payload(payload):
        success = False
        output_values = []
        number_of_values = int.from_bytes(payload[0:1], byteorder='big',
                                        signed=False)
        # Each output value is 4 Bytes long.
        if number_of_values == (len(payload[1:]) / 4):
            # Iterate over 32 Bit integers: 4 Bytes per encoded value, 1 byte
            # offset to first payload Byte.
            for value_index in range(number_of_values):
                output_values.append(int.from_bytes(payload[((value_index * 4) + 1):
                    (((value_index + 1) * 4) + 1)], byteorder='big', signed=False))
            print("Output values: ", output_values)
            success = True
        return success


    def process_get_status_payload(payload):
        success = False
        if len(payload) >= 10:  # Minimum payload length: 10 Byte.
            status = int.from_bytes(payload[0:1], byteorder='big', signed=False)
            error_flag = (status >> 7) & 0x01
            status_group = (status >> 3) & 0x0f
            status_sub_group = status & 0x7
            rx_sequence_number = int.from_bytes(payload[1:2], byteorder='big',
                                                signed=False)
            rx_result = int.from_bytes(payload[2:3], byteorder='big', signed=True)
            last_reached_waypoint = int.from_bytes(payload[3:4], byteorder='big',
                                                signed=False)
            last_error_status_sequence_number = int.from_bytes(payload[4:5],
                                                            byteorder='big',
                                                            signed=False)
            last_error_status = int.from_bytes(payload[5:6], byteorder='big',
                                            signed=False)
            last_error_flag = (last_error_status >> 7) & 0x01
            last_error_status_gorup = (last_error_status >> 3) & 0x0f
            last_error_status_sub_gorup = last_error_status & 0x07
            mapped_data_id = int.from_bytes(payload[6:7], byteorder='big',
                                            signed=False)
            mapped_data_length = int.from_bytes(payload[7:9], byteorder='big',
                                                signed=False)
            mapped_data = payload[9:]
            print("Status: Error:", error_flag, "Group:", status_group,"Sub-Group:",
                    status_sub_group, "Rx Sequence Number:", rx_sequence_number,
                    "Rx Result:", rx_result, "Last Reached Waypoint:",
                    last_reached_waypoint, "Last Error Sequence Number",
                    last_error_status_sequence_number, "Last Error Flag:",
                    last_error_flag, "Last Error Group:", last_error_status_gorup,
                    "Last Error Sub-Group:", last_error_status_sub_gorup,
                    "Mapped Data ID:", mapped_data_id, "Mapped Data Length:",
                    mapped_data_length, "Mapped Data:", mapped_data)
            success = True
        return success


    def decode_angular_value(raw_angular_value):
        # Angular values are encoded as nano radians divided by pi.
        return raw_angular_value * 1e-9 * math.pi


    def decode_linear_value(raw_linear_value):
        # Linear values are encoded as micro meters.
        return raw_linear_value * 1e-6


