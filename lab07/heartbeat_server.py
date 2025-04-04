import socket
import time
from collections import defaultdict


class HeartbeatServer:
    def __init__(self, host='localhost', port=12000, timeout=5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.clients = defaultdict(dict)

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind((self.host, self.port))
            print(f"Heartbeat server listening on {self.host}:{self.port}")

            while True:
                try:
                    data, addr = sock.recvfrom(1024)
                    current_time = time.time()
                    client_id = f"{addr[0]}:{addr[1]}"

                    try:
                        seq_num, timestamp = data.decode().split(',')
                        timestamp = float(timestamp)
                        delay = current_time - timestamp

                        self.clients[client_id]['last_seen'] = current_time
                        self.clients[client_id]['delay'] = delay
                        self.clients[client_id]['seq'] = seq_num

                        print(f"Heartbeat from {client_id} seq={seq_num} delay={delay:.3f}s")

                    except ValueError:
                        print(f"Invalid data from {client_id}")

                    self.check_timeouts(current_time)

                except KeyboardInterrupt:
                    print("\nServer shutting down...")
                    break
                except Exception as e:
                    print(f"Error: {e}")

    def check_timeouts(self, current_time):
        timed_out = []
        for client_id, client_data in self.clients.items():
            if current_time - client_data['last_seen'] > self.timeout:
                timed_out.append(client_id)
                print(f"Client {client_id} timed out (last seq={client_data['seq']})")

        for client_id in timed_out:
            del self.clients[client_id]


if __name__ == "__main__":
    server = HeartbeatServer()
    server.start()