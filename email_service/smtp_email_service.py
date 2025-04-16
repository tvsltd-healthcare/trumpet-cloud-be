import os
import smtplib
from email.mime.text import MIMEText
from email_service.templates.email_template import EMAIL_TEMPLATE
from domain_layer.abstractions.email_sending_interface import IEmailService
from dotenv import load_dotenv
load_dotenv()

# Email configurations
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
EMAIL_SUBJECT = os.getenv("EMAIL_SUBJECT")

class SmtpEmailService:
    def __init__(self):
        self.host = EMAIL_HOST
        self.port = EMAIL_PORT
        self.username = EMAIL_USERNAME
        self.password = EMAIL_PASSWORD
        # self.subject = EMAIL_SUBJECT
        # self.sender_email = SENDER_EMAIL

    def send_email(self, to_email: str, body: str ) -> None:
        
        # Create email message
        msg = MIMEText(EMAIL_TEMPLATE.format(token=body), "html")
        msg["Subject"] = EMAIL_SUBJECT
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email

        # Connect to SMTP server and send email
        try:
            with smtplib.SMTP(self.host, self.port) as server:
                server.login(self.username, self.password)
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")