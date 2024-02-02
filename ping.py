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
    # Craft an ICMP packet with a simple structure
    icmp_type = 8  # ICMP Echo Request
    icmp_code = 0
    icmp_checksum = 0
    icmp_id = 12345
    icmp_seq = 1
    data = b'Hello, ICMP!'

    # Create the ICMP header
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

    # Calculate checksum for the header and data
    checksum_data = icmp_header + data
    icmp_checksum = calculate_checksum(checksum_data)

    # Recreate the ICMP header with the correct checksum
    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq)

    # Combine the header and data to form the complete packet
    icmp_packet = icmp_header + data

    return icmp_packet

