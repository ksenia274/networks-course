import socket
import base64

# Конфигурация SMTP сервера
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'kcen.yackubowa2013@gmail.com'
SENDER_PASSWORD = 'sdxg dviv utsv jmhj'

def send_email(recipient_email, subject, message):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SMTP_SERVER, SMTP_PORT))
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.send(b'EHLO example.com\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.send(b'STARTTLS\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        import ssl
        client_socket = ssl.wrap_socket(client_socket)

        client_socket.send(b'EHLO example.com\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.send(b'AUTH LOGIN\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.send(base64.b64encode(SENDER_EMAIL.encode()) + b'\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.send(base64.b64encode(SENDER_PASSWORD.encode()) + b'\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.send(f'MAIL FROM: <{SENDER_EMAIL}>\r\n'.encode())
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.send(f'RCPT TO: <{recipient_email}>\r\n'.encode())
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.send(b'DATA\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        email_body = f"From: {SENDER_EMAIL}\r\nTo: {recipient_email}\r\nSubject: {subject}\r\n\r\n{message}\r\n.\r\n"
        client_socket.send(email_body.encode())
        response = client_socket.recv(1024).decode()
        print(response)

        # Завершаем сессию
        client_socket.send(b'QUIT\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        print(f"Email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    recipient_email = input("Enter recipient email: ")
    subject = "Test Email"
    message = "This is a plain text email."

    send_email(recipient_email, subject, message)