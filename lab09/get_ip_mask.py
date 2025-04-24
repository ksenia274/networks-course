import socket
import netifaces


def get_ip_and_netmask():
    hostname = socket.gethostname()

    interfaces = netifaces.interfaces()

    for interface in interfaces:
        if interface == 'lo':
            continue

        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            for addr_info in addrs[netifaces.AF_INET]:
                ip = addr_info.get('addr')
                netmask = addr_info.get('netmask')
                if ip and netmask:
                    print(f"Интерфейс: {interface}")
                    print(f"IP-адрес: {ip}")
                    print(f"Маска подсети: {netmask}")
                    print()


if __name__ == "__main__":
    try:
        get_ip_and_netmask()
    except Exception as e:
        print(f"Произошла ошибка: {e}")