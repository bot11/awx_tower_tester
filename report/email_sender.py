import smtplib
from email.message import EmailMessage

class EmailSender:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password, use_tls=True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password
        self.use_tls = use_tls

    def send_email(self, subject, body, to_addresses):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.smtp_username
        msg['To'] = to_addresses
        msg.set_content(body)

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            if self.use_tls:
                server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            server.send_message(msg)
