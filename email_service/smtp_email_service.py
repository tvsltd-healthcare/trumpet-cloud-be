import smtplib
from email.mime.text import MIMEText
from typing import Dict
from email_service.templates.email_template import EMAIL_TEMPLATE
from domain_layer.abstractions.email_sending_interface import IEmailService

class SmtpEmailService(IEmailService):
    def __init__(self, config: Dict):
        self.config = config

    def send_email(self, to_email: str, body: str ) -> None:
        
        # Create email message
        msg = MIMEText(EMAIL_TEMPLATE.format(token=body), "html")
        msg["Subject"] = self.config["subject"]
        msg["From"] = self.config["sender_email"]
        msg["To"] = to_email

        # Connect to SMTP server and send email
        try:
            with smtplib.SMTP(self.config["host"], self.config["port"]) as server:
                server.login(self.config["username"], self.config["password"])
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
