import socket
import struct
import time
import sys

def calculate_checksum(data):
    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8) + data[i + 1]
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    return checksum

def create_icmp_packet():
    icmp_type = 8
    icmp_code = 0
    icmp_checksum = 0
    icmp_id = 12345
    icmp_seq = 1
    data = b'Hello, ICMP!'

    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

    checksum_data = icmp_header + data
    icmp_checksum = calculate_checksum(checksum_data)

    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

    icmp_packet = icmp_header + data

    return icmp_packet

def is_valid_ip(ip):

    try:
        socket.inet_pton(socket.AF_INET, ip)
        return True

    except socket.error:
        return False

def create_icmp_packet(seq_num):
    # Craft an ICMP packet with a simple structure
    icmp_type = 8  # ICMP Echo Request
    icmp_code = 0
    icmp_checksum = 0
    icmp_id = 12345
    data = b'Hello, ICMP!'

    # Create the ICMP header
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, seq_num)

    # Calculate checksum for the header and data
    checksum_data = icmp_header + data
    icmp_checksum = calculate_checksum(checksum_data)

    # Recreate the ICMP header with the correct checksum
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, seq_num)

    # Combine the header and data to form the complete packet
    icmp_packet = icmp_header + data

    return icmp_packet


