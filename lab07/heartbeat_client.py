import socket
import time
import random


class HeartbeatClient:
    def __init__(self, server_host='localhost', server_port=12000, interval=1):
        self.server_host = server_host
        self.server_port = server_port
        self.interval = interval
        self.seq_num = 0

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.settimeout(1)
            print(f"Heartbeat client sending to {self.server_host}:{self.server_port}")

            while True:
                try:
                    self.seq_num += 1
                    timestamp = time.time()
                    message = f"{self.seq_num},{timestamp}"

                    if random.random() > 0.1:
                        sock.sendto(message.encode(), (self.server_host, self.server_port))
                        print(f"Sent heartbeat seq={self.seq_num}")
                    else:
                        print(f"Packet loss simulated seq={self.seq_num}")

                    time.sleep(self.interval)

                except KeyboardInterrupt:
                    print("\nClient stopping...")
                    break
                except Exception as e:
                    print(f"Error: {e}")
                    time.sleep(1)


if __name__ == "__main__":
    client = HeartbeatClient(interval=random.uniform(0.5, 2))
    client.start()