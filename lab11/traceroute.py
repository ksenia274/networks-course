import socket
import struct
import time
import select
import os

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11
MAX_HOPS = 30
TRIES_PER_HOP = 3
TIMEOUT = 2.0

def checksum(source):
    sum = 0
    countTo = (len(source) // 2) * 2
    for count in range(0, countTo, 2):
        thisVal = source[count + 1] * 256 + source[count]
        sum = sum + thisVal
        sum = sum & 0xffffffff
    if countTo < len(source):
        sum = sum + source[-1]
        sum = sum & 0xffffffff
    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    return answer >> 8 | (answer << 8 & 0xff00)

def create_packet(id):
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, id, 1)
    data = struct.pack("d", time.time())
    my_checksum = checksum(header + data)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, 1)
    return header + data

def traceroute(dest_name, tries=TRIES_PER_HOP):
    try:
        dest_addr = socket.gethostbyname(dest_name)
    except socket.gaierror:
        print(f"Unable to resolve {dest_name}")
        return
    print(f"Tracing route to {dest_name} [{dest_addr}] with {tries} packets per hop:")

    for ttl in range(1, MAX_HOPS + 1):
        print(f"{ttl:2}", end="  ")
        reached = False

        for attempt in range(tries):
            recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            send_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            send_socket.setsockopt(socket.IPPROTO_IP, socket.IP_TTL, ttl)
            recv_socket.settimeout(TIMEOUT)

            pid = os.getpid() & 0xFFFF
            packet = create_packet(pid)
            send_time = time.time()

            try:
                send_socket.sendto(packet, (dest_addr, 0))
                recv_socket.bind(("", 0))
                start = time.time()
                ready = select.select([recv_socket], [], [], TIMEOUT)
                if ready[0] == []:
                    print("*", end="  ")
                else:
                    recv_packet, addr = recv_socket.recvfrom(1024)
                    rtt = (time.time() - send_time) * 1000
                    icmp_header = recv_packet[20:28]
                    icmp_type, _, _, _, _ = struct.unpack("bbHHh", icmp_header)
                    print(f"{rtt:.2f}ms", end=" ")

                    if icmp_type == ICMP_ECHO_REPLY:
                        reached = True

            except socket.error as e:
                print("Error:", e)
                break
            finally:
                recv_socket.close()
                send_socket.close()

        print()
        if reached:
            break

if __name__ == "__main__":
    destination = input("Enter host to traceroute: ")
    traceroute(destination)