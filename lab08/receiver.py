import socket
import random

HOST = '127.0.0.1'
PORT = 12345
OUTPUT_FILE = 'received_file.txt'

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((HOST, PORT))
    print("Сервер запущен и ожидает подключения...")

    expected_seq_num = 0
    received_data = b''

    with open(OUTPUT_FILE, 'wb') as output_file:
        while True:
            packet, client_address = server_socket.recvfrom(1024)
            seq_num = packet[0]
            data = packet[1:]

            if random.random() < 0.3:
                print("Пакет потерян")
                continue


            if seq_num == expected_seq_num:
                received_data += data
                output_file.write(data)
                ack_packet = bytes([expected_seq_num])
                server_socket.sendto(ack_packet, client_address)
                print(f"Отправлен ACK для пакета {expected_seq_num}")
                expected_seq_num ^= 1
            else:
                print(f"Игнорируется пакет {seq_num}, ожидается {expected_seq_num}")

if __name__ == "__main__":
    main()