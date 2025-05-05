import os
import smtplib
from email.mime.text import MIMEText
from typing import Dict
from email_service.templates.varify_org_email_template import VARIFY_ORG_EMAIL_TEMPLATE
from email_service.templates.varify_researcher_email_template import VARIFY_RESEARCHER_EMAIL_TEMPLATE
from domain_layer.abstractions.email_sending_interface import IEmailService

class SmtpEmailService(IEmailService):
    def __init__(self, config: Dict):
        self.config = config
        self.template_map = {
            'varify_org': {
                'template': VARIFY_ORG_EMAIL_TEMPLATE,
                'subject': 'Varify your organization on Trumpet Cloud'
            },

            'varify_researcher': {
                'template': VARIFY_RESEARCHER_EMAIL_TEMPLATE,
                'subject': 'Varify your researcher on Trumpet Cloud'
            }
        }

    def send_email(self, to_email: str, body: str, type: str ) -> None:
        template, subject = self.template_map.get(type).values()
        print("template:")
        print(template)
        print("subject:")
        print(subject)

        # sub = self.template_map.get(type).get('subject')

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
