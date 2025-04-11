import socket
import time
import os
import random

HOST = '127.0.0.1'
PORT = 12345
TIMEOUT = 1


def send_file(filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    with open(filename, 'rb') as f:
        seq_num = 0
        while True:
            data = f.read(1024)
            if not data:
                break

            packet = bytes([seq_num]) + data

            while True:
                client_socket.sendto(packet, (HOST, PORT))

                client_socket.settimeout(TIMEOUT)
                try:
                    ack_packet, _ = client_socket.recvfrom(1)
                    ack_num = ack_packet[0]
                    print(f"Получен ACK для пакета {ack_num}")
                    if ack_num == seq_num:
                        seq_num ^= 1
                        break
                except socket.timeout:
                    print(f"Таймаут! Повторная отправка пакета {seq_num}")

    client_socket.close()
    print("Передача завершена.")


if __name__ == "__main__":
    send_file('good_file.txt')