import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'kcen.yackubowa2013@gmail.com'
SENDER_PASSWORD = 'sdxg dviv utsv jmhj'


def send_email(recipient_email, subject, message, message_format='txt'):
    try:
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = recipient_email
        msg['Subject'] = subject

        if message_format == 'txt':
            msg.attach(MIMEText(message, 'plain'))
        elif message_format == 'html':
            msg.attach(MIMEText(message, 'html'))
        else:
            raise ValueError("Unsupported message format. Use 'txt' or 'html'.")

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, recipient_email, msg.as_string())
            print(f"Email sent successfully to {recipient_email}")

    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    recipient_email = input("Enter recipient email: ")
    subject = "Test Email"
    message_txt = "This is a plain text email."
    message_html = "<html><body><h1>This is a HTML email.</h1></body></html>"

    send_email(recipient_email, subject, message_txt, 'txt')
    send_email(recipient_email, subject, message_html, 'html')