import socket
import sys


def send_file(filename, client_socket):
    try:
        with open(filename, 'rb') as file:
            content = file.read()
            response = (
                "HTTP/1.1 200 OK\r\n"
                f"Content-Length: {len(content)}\r\n\r\n"
            )
            client_socket.sendall(response.encode('utf-8'))
            client_socket.sendall(content)
    except FileNotFoundError:
        response = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n404 Not Found"
        client_socket.sendall(response.encode('utf-8'))


def handle_request(client_socket):
    request = client_socket.recv(1024).decode('utf-8')
    filename = request.split()[1]
    send_file(filename.lstrip('/'), client_socket)


def main(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', int(port))
    server_socket.bind(server_address)
    print(f"Server started on http://{server_address[0]}:{port}")

    server_socket.listen(1)
    while True:
        print("Waiting for a connection...")
        connection, client_address = server_socket.accept()
        try:
            print(f'Connection from {client_address}')
            handle_request(connection)
        finally:
            connection.close()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f"{sys.argv[0]} <port>")
        sys.exit(1)

    main(sys.argv[1])