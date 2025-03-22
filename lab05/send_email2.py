import socket
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'kcen.yackubowa2013@gmail.com'
SENDER_PASSWORD = 'sdxg dviv utsv jmhj'

def send_email(recipient_email, subject, text_message, image_path):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(text_message, 'plain'))

        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            image = MIMEImage(img_data, name=image_path.split('/')[-1])
            msg.attach(image)

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

        client_socket.send(msg.as_string().encode())
        client_socket.send(b'\r\n.\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        client_socket.send(b'QUIT\r\n')
        response = client_socket.recv(1024).decode()
        print(response)

        print(f"Email with image sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")

    finally:
        client_socket.close()

if __name__ == "__main__":
    recipient_email = input("Enter recipient email: ")
    subject = "Test Email with Image"
    text_message = "This is a test email with an image attachment."
    image_path = input("Enter the path to the image file: ")

    send_email(recipient_email, subject, text_message, image_path)