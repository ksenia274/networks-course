import subprocess
import threading
import sys


def start_client(interval):

    subprocess.run(["python", "heartbeat_client.py", str(interval)])


if __name__ == "__main__":
    # Запуск 3 клиентов с разными интервалами (1, 1.5 и 2 секунды)
    intervals = [1, 1.5, 2]

    for interval in intervals:
        threading.Thread(target=start_client, args=(interval,)).start()

    print(f"Started {len(intervals)} clients with intervals {intervals}")