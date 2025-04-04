import socket
import time


def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)

    server_address = ('localhost', 12000)

    for sequence_number in range(1, 11):
        send_time = time.time()
        message = f"Ping {sequence_number} {send_time}"

        try:
            client_socket.sendto(message.encode(), server_address)

            try:
                modified_message, server = client_socket.recvfrom(1024)
                receive_time = time.time()
                rtt = receive_time - send_time
                print(f"Reply from {server}: {modified_message.decode()}")
                print(f"RTT: {rtt:.6f} seconds\n")
            except socket.timeout:
                print("Request timed out\n")

        except Exception as e:
            print(f"Error sending packet {sequence_number}: {e}\n")


if __name__ == "__main__":
    udp_client()