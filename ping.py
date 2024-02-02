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
