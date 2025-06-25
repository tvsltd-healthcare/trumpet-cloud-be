import os
import smtplib
from typing import Dict
from email.mime.text import MIMEText
from domain_layer.abstractions.email_sending_interface import IEmailService
from email_service.templates.email_template_map import EMAIL_TEMPLATE_MAP

class SmtpEmailService(IEmailService):
    def __init__(self, config: Dict):
        self.config = config
        self.template_map = EMAIL_TEMPLATE_MAP

    def send_email(self, to_email: str, body: str, type: str) -> None:
        """
        Sends an email using an SMTP server based on the given email type and recipient.

        This method selects an HTML template and subject from a predefined template map,
        formats the template using the provided token and environment host, and sends the
        email using the configured SMTP server.

        Args:
            to_email (str): The recipient's email address.
            body (str): A token or value to inject into the email template (e.g., a reset token).
            type (str): The type of email to send (e.g., 'reset_password', 'varify_org', etc.),
                        used to look up the corresponding template and subject.

        Raises:
            Exception: If sending the email fails due to an SMTP connection or authentication error.
        """
        template, subject = self.template_map.get(type).values()

        # Create email message
        msg = MIMEText(template.format(token=body, host=os.getenv("TRUMPET_CLOUD_WEBSITE_HOST")), "html")
        msg["Subject"] = subject
        msg["From"] = self.config["sender_email"]
        msg["To"] = to_email

        # Connect to SMTP server and send email
        try:
            with smtplib.SMTP(self.config["host"], self.config["port"]) as server:
                server.login(self.config["username"], self.config["password"])
                server.send_message(msg)
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")
