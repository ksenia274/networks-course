import socket
import random
import time


def udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 12000))

    print("Server is ready to receive")

    while True:
        message, client_address = server_socket.recvfrom(1024)
        print(f"Received message from {client_address}")

        # Моделируем 20% потерю пакетов
        if random.random() < 0.2:
            print("Packet lost (simulated)")
            continue

        modified_message = message.decode().upper()
        server_socket.sendto(modified_message.encode(), client_address)


if __name__ == "__main__":
    udp_server()