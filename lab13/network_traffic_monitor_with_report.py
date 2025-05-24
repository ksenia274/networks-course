import psutil
import time
from collections import defaultdict


def get_conn_stats():
    conns = psutil.net_connections(kind='inet')
    port_traffic = defaultdict(lambda: {'sent': 0, 'recv': 0})

    for conn in conns:
        laddr = conn.laddr.port if conn.laddr else None
        raddr = conn.raddr.port if conn.raddr else None

        pid = conn.pid
        if pid is not None:
            try:
                proc = psutil.Process(pid)
                io_counters = proc.io_counters()
                sent = io_counters.other_write_bytes if hasattr(io_counters,
                                                                'other_write_bytes') else io_counters.write_bytes
                recv = io_counters.other_read_bytes if hasattr(io_counters,
                                                               'other_read_bytes') else io_counters.read_bytes
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

            if laddr:
                port_traffic[laddr]['sent'] += sent
                port_traffic[laddr]['recv'] += recv
            if raddr:
                port_traffic[raddr]['recv'] += recv
                port_traffic[raddr]['sent'] += sent

    return port_traffic


def format_bytes(num):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return f"{num:.2f} {unit}"
        num /= 1024.0
    return f"{num:.2f} TB"


def main():
    print("Сбор статистики по портам. Ctrl+C для выхода.")
    try:
        while True:
            traffic = get_conn_stats()
            print("\nОтчет по портам:")
            print(f"{'Порт':<10}{'Отправлено':<20}{'Получено'}")
            for port, stats in sorted(traffic.items()):
                print(f"{port:<10}{format_bytes(stats['sent']):<20}{format_bytes(stats['recv'])}")
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nЗавершено пользователем.")

if __name__ == "__main__":
    main()