import psutil
import time
import datetime

def get_network_bytes():
    counters = psutil.net_io_counters()
    return counters.bytes_sent, counters.bytes_recv

def format_bytes(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"

def main():
    print("Мониторинг сетевого трафика. Ctrl+C для выхода.")
    sent0, recv0 = get_network_bytes()
    try:
        while True:
            time.sleep(1)
            sent1, recv1 = get_network_bytes()
            sent_speed = sent1 - sent0
            recv_speed = recv1 - recv0
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] ↑ {format_bytes(sent_speed)}/s ↓ {format_bytes(recv_speed)}/s")
            sent0, recv0 = sent1, recv1
    except KeyboardInterrupt:
        print("\nЗавершено пользователем.")

if __name__ == "__main__":
    main()