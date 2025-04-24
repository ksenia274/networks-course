import socket
import argparse


def check_ports(ip, start_port, end_port):
    free_ports = []
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            try:
                s.connect((ip, port))
            except (socket.timeout, ConnectionRefusedError):
                free_ports.append(port)
            except Exception as e:
                print(f"Ошибка при проверке порта {port}: {e}")
    return free_ports


def main():
    parser = argparse.ArgumentParser(description='Проверка свободных портов')
    parser.add_argument('ip', help='IP-адрес для проверки')
    parser.add_argument('start_port', type=int, help='Начальный порт диапазона')
    parser.add_argument('end_port', type=int, help='Конечный порт диапазона')

    args = parser.parse_args()

    if args.start_port > args.end_port:
        print("Ошибка: начальный порт должен быть меньше или равен конечному")
        return

    if not (0 < args.start_port <= 65535 and 0 < args.end_port <= 65535):
        print("Ошибка: порты должны быть в диапазоне 1-65535")
        return

    print(f"Проверка свободных портов на {args.ip} с {args.start_port} по {args.end_port}...")
    free_ports = check_ports(args.ip, args.start_port, args.end_port)

    print("\nСвободные порты:")
    if free_ports:
        print(', '.join(map(str, free_ports)))
    else:
        print("Нет свободных портов в указанном диапазоне")


if __name__ == "__main__":
    main()