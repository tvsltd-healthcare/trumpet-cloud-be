import os
import smtplib
import asyncio
from typing import Dict
from email.mime.text import MIMEText
from azure.communication.email import EmailClient
from domain_layer.abstractions.email_sending_interface import IEmailService
from email_service.templates.varify_org_email_template import VARIFY_ORG_EMAIL_TEMPLATE
from email_service.templates.reset_password_email_template import RESET_PASSWORD_EMAIL_TEMPLATE
from email_service.templates.varify_researcher_email_template import VARIFY_RESEARCHER_EMAIL_TEMPLATE
from email_service.templates.registration_approved_email_templlate import REGISTRATION_APPROVED_EMAIL_TEMPLATE
from email_service.templates.registration_disapproved_email_templlate import DISAPPROVED_REGISTRATION_EMAIL_TEMPLATE

class SmtpEmailService(IEmailService):
    def __init__(self, config: Dict):
        self.config = config
        self.template_map = {
            'varify_org': {
                'template': VARIFY_ORG_EMAIL_TEMPLATE,
                'subject': 'Verify your organization on Trumpet Cloud'
            },
            'varify_researcher': {
                'template': VARIFY_RESEARCHER_EMAIL_TEMPLATE,
                'subject': 'Verify your researcher on Trumpet Cloud'
            },
            'approved_registration': {
                'template': REGISTRATION_APPROVED_EMAIL_TEMPLATE,
                'subject': 'Your registration has been successfully approved.'
            },

            'disapproved_registration': {
                'template': DISAPPROVED_REGISTRATION_EMAIL_TEMPLATE,
                'subject': 'Your registration has not been approved'
            },
            'reset_password': {
                'template': RESET_PASSWORD_EMAIL_TEMPLATE,
                'subject': 'Reset password.'
            }
        }

    def send_email(self, to_email: str, body: str, type: str) -> None:

        try:
            if(self.config.get('node_env') == 'production'):
                asyncio.create_task(self.send_email_via_azure(to_email, body, type))
            elif(self.config.get('node_env') == 'development'):
                self.send_email_via_smtp(to_email, body, type)
        except Exception as e:
            print("Email send failed:", e)


    async def send_email_via_azure(self, to_email: str, body: str, type: str):

        template, subject = self.template_map.get(type).values()
        message = {
            "senderAddress": self.config.get('sender_email'),
            "content": {
                "subject": subject,
                "html": template
            },
            "recipients": {
                "to": [{"address": "mdtajalislam1189@gmail.com" }]
            }
        }
        email_client = EmailClient.from_connection_string(self.config.get('azure_connection_string'))

        try:
            email_client.begin_send(message)
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")


    def send_email_via_smtp(self, to_email: str, body: str, type: str ) -> None:
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
