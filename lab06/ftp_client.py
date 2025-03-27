import socket
import os
import sys
from datetime import datetime


class FTPClient:
    def __init__(self):
        self.control_socket = None
        self.data_socket = None
        self.pasv_port = 0
        self.pasv_ip = ""
        self.connected = False
        self.username = None
        self.password = None

    def connect(self, host, port=21):
        try:
            self.control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.control_socket.connect((host, port))
            response = self._get_response()
            print(response)
            self.connected = True
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def login(self, username, password):
        self.username = username
        self.password = password
        self._send_command(f"USER {username}")
        response = self._get_response()
        print(response)

        self._send_command(f"PASS {password}")
        response = self._get_response()
        print(response)

        if "230" in response:
            return True
        return False

    def list_files(self):
        if not self._enter_pasv_mode():
            return False

        self._send_command("LIST")
        response = self._get_response()
        print(response)

        data = self._receive_data()
        print(data.decode('utf-8'))

        response = self._get_response()
        print(response)
        return True

    def upload_file(self, local_path, remote_path):
        if not os.path.exists(local_path):
            print(f"Local file {local_path} does not exist")
            return False

        if not self._enter_pasv_mode():
            return False

        self._send_command(f"STOR {remote_path}")
        response = self._get_response()
        print(response)

        try:
            with open(local_path, 'rb') as file:
                data = file.read()
                self.data_socket.sendall(data)

            self.data_socket.close()
            response = self._get_response()
            print(response)
            return True
        except Exception as e:
            print(f"Upload error: {e}")
            return False

    def download_file(self, remote_path, local_path):
        if not self._enter_pasv_mode():
            return False

        self._send_command(f"RETR {remote_path}")
        response = self._get_response()
        print(response)

        try:
            with open(local_path, 'wb') as file:
                while True:
                    data = self.data_socket.recv(1024)
                    if not data:
                        break
                    file.write(data)

            self.data_socket.close()
            response = self._get_response()
            print(response)
            return True
        except Exception as e:
            print(f"Download error: {e}")
            return False

    def quit(self):
        self._send_command("QUIT")
        response = self._get_response()
        print(response)
        self.control_socket.close()
        self.connected = False

    def _enter_pasv_mode(self):
        self._send_command("PASV")
        response = self._get_response()
        print(response)

        if "227" not in response:
            return False

        start = response.find('(')
        end = response.find(')')
        if start == -1 or end == -1:
            return False

        parts = response[start + 1:end].split(',')
        if len(parts) < 6:
            return False

        ip = ".".join(parts[:4])
        port = (int(parts[4]) << 8) + int(parts[5])

        try:
            self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.data_socket.connect((ip, port))
            return True
        except Exception as e:
            print(f"Data connection error: {e}")
            return False

    def _send_command(self, command):
        if not self.connected:
            print("Not connected to server")
            return

        print(f"> {command}")
        self.control_socket.sendall((command + "\r\n").encode('utf-8'))

    def _get_response(self):
        if not self.connected:
            return "Not connected to server"

        response = ""
        while True:
            part = self.control_socket.recv(1024).decode('utf-8')
            response += part
            if '\n' in part:
                break
        return response.strip()

    def _receive_data(self):
        data = b""
        while True:
            part = self.data_socket.recv(4096)
            if not part:
                break
            data += part
        return data


def print_help():
    print("\nAvailable commands:")
    print("  connect <host> [port] - Connect to FTP server")
    print("  login <username> <password> - Login to FTP server")
    print("  list - List files on the server")
    print("  upload <local_path> <remote_path> - Upload file to server")
    print("  download <remote_path> <local_path> - Download file from server")
    print("  quit - Disconnect from server")
    print("  help - Show this help")
    print("  exit - Exit the program")


def main():
    print("Simple FTP Client (using raw sockets)")
    print("Type 'help' for list of commands")

    ftp = FTPClient()

    while True:
        try:
            command = input("ftp> ").strip()
            if not command:
                continue

            parts = command.split()
            cmd = parts[0].lower()

            if cmd == "help":
                print_help()
            elif cmd == "exit":
                if ftp.connected:
                    ftp.quit()
                break
            elif cmd == "connect":
                if len(parts) < 2:
                    print("Usage: connect <host> [port]")
                    continue
                host = parts[1]
                port = int(parts[2]) if len(parts) > 2 else 21
                ftp.connect(host, port)
            elif cmd == "login":
                if len(parts) < 3:
                    print("Usage: login <username> <password>")
                    continue
                username = parts[1]
                password = parts[2]
                ftp.login(username, password)
            elif cmd == "list":
                if not ftp.connected:
                    print("Not connected to server")
                    continue
                ftp.list_files()
            elif cmd == "upload":
                if len(parts) < 3:
                    print("Usage: upload <local_path> <remote_path>")
                    continue
                local_path = parts[1]
                remote_path = parts[2]
                ftp.upload_file(local_path, remote_path)
            elif cmd == "download":
                if len(parts) < 3:
                    print("Usage: download <remote_path> <local_path>")
                    continue
                remote_path = parts[1]
                local_path = parts[2]
                ftp.download_file(remote_path, local_path)
            elif cmd == "quit":
                if ftp.connected:
                    ftp.quit()
                else:
                    print("Not connected to server")
            else:
                print(f"Unknown command: {cmd}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()