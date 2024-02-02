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
    icmp_type = 8
    icmp_code = 0
    icmp_checksum = 0
    icmp_id = 12345
    data = b'Hello, ICMP!'

    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, seq_num)

    checksum_data = icmp_header + data
    icmp_checksum = calculate_checksum(checksum_data)

    icmp_header = struct.pack('!BBHHH', icmp_type, icmp_code, icmp_checksum, icmp_id, seq_num)

    icmp_packet = icmp_header + data

    return icmp_packet

def send_ping(target_host, count):
    if is_valid_ip(target_host):
        target_ip = target_host
    else:
        try:
            # Get the IP address of the target host
            target_ip = socket.gethostbyname(target_host)
        except socket.gaierror as e:
            print(f"Error: {e}")
            return

    # Create a raw socket
    icmp_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

    # Set the timeout for receiving packets
    icmp_socket.settimeout(1)

    success_count = 0

    for seq_num in range(1, count + 1):
        # Craft the ICMP packet with a unique sequence number
        icmp_packet = create_icmp_packet(seq_num)

        try:
            # Send the packet to the target
            icmp_socket.sendto(icmp_packet, (target_ip, 0))

            # Record the time when the packet was sent
            send_time = time.time()

            # Receive the response
            response, addr = icmp_socket.recvfrom(1024)

            # Calculate round-trip time
            rtt = (time.time() - send_time) * 1000  # Convert to milliseconds

            # Print the results
            print(f"Ping successful.Reply from {addr}: time={rtt:.2f}ms")
            success_count += 1

        except socket.timeout:
            print("\nRequest timed out.")

    # Calculate packet loss percentage
    packet_loss_percentage = ((count - success_count) / count) * 100

    # Print summary
    print(f"\n--- Ping statistics for {target_host} ---")
    print(f"Packets: Sent = {count}, Received = {success_count}, Lost = {count - success_count} ({packet_loss_percentage:.2f}% loss)")

    # Close the socket after all pings
    icmp_socket.close()

