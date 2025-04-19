import socket
import threading
import time
import json

BROADCAST_ADDRESS = '255.255.255.255'
PORT = 5000
MESSAGE_INTERVAL = 2
TIMEOUT = 5

active_apps = {}


def broadcast_message(message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(message.encode(), (BROADCAST_ADDRESS, PORT))


def listen_for_messages():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', PORT))
        while True:
            data, addr = sock.recvfrom(1024)
            message = json.loads(data.decode())
            if message['type'] == 'start':
                handle_start_message(addr)
            elif message['type'] == 'stop':
                handle_stop_message(addr)


def handle_start_message(addr):
    ip = addr[0]
    active_apps[ip] = time.time()
    print(f"Приложение запущено на {ip}:{PORT}")
    print_active_apps_count()
    response_message = json.dumps({'type': 'alive'})
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.sendto(response_message.encode(), addr)


def handle_stop_message(addr):
    ip = addr[0]
    if ip in active_apps:
        del active_apps[ip]
        print(f"Приложение завершило работу на {ip}:{PORT}")
        print_active_apps_count()


def send_broadcast():
    message = json.dumps({'type': 'start'})
    while True:
        broadcast_message(message)
        time.sleep(MESSAGE_INTERVAL)


def cleanup():
    current_time = time.time()
    inactive_ips = [ip for ip, last_seen in active_apps.items() if current_time - last_seen > TIMEOUT]
    for ip in inactive_ips:
        del active_apps[ip]
        print(f"Приложение неактивно: {ip}:{PORT}")
    print_active_apps_count()


def print_active_apps_count():
    count = len(active_apps)
    print(f"Количество активных приложений: {count}")


if __name__ == "__main__":
    threading.Thread(target=listen_for_messages, daemon=True).start()

    threading.Thread(target=send_broadcast, daemon=True).start()

    try:
        while True:
            cleanup()
            time.sleep(1)
    except KeyboardInterrupt:
        stop_message = json.dumps({'type': 'stop'})
        broadcast_message(stop_message)
        print("Завершение работы приложения.")