import socket
import time
import statistics


def udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)

    server_address = ('localhost', 12000)
    rtt_list = []
    lost_packets = 0

    print(f"Pinging {server_address[0]} with {10} packets\n")

    for sequence_number in range(1, 11):
        send_time = time.time()
        message = f"Ping {sequence_number} {send_time}"

        try:
            client_socket.sendto(message.encode(), server_address)

            try:
                modified_message, server = client_socket.recvfrom(1024)
                receive_time = time.time()
                rtt = (receive_time - send_time) * 1000  # Конвертируем в миллисекунды
                rtt_list.append(rtt)
                print(f"Reply from {server_address[0]}: bytes={len(message)} time={rtt:.2f}ms TTL=64")
            except socket.timeout:
                lost_packets += 1
                print("Request timed out.")

        except Exception as e:
            lost_packets += 1
            print(f"Error sending packet {sequence_number}: {e}")


    print("\nPing statistics for", server_address[0])
    packets_sent = 10
    packets_received = packets_sent - lost_packets
    loss_percentage = (lost_packets / packets_sent) * 100
    print(
        f"    Packets: Sent = {packets_sent}, Received = {packets_received}, Lost = {lost_packets} ({loss_percentage:.0f}% loss)")

    if rtt_list:
        print("Approximate round trip times in milli-seconds:")
        print(
            f"    Minimum = {min(rtt_list):.2f}ms, Maximum = {max(rtt_list):.2f}ms, Average = {statistics.mean(rtt_list):.2f}ms")


if __name__ == "__main__":
    udp_client()