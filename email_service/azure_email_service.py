import os
from typing import Dict
from azure.communication.email import EmailClient
from email_service.templates.email_template_map import EMAIL_TEMPLATE_MAP
from domain_layer.abstractions.email_sending_interface import IEmailService

class AzureEmailService(IEmailService):
    def __init__(self, config: Dict):
        self.config = config
        self.template_map = EMAIL_TEMPLATE_MAP

    def send_email(self, to_email: str, body: str, type: str) -> None:
        """
        Sends an email to the specified recipient using Azure Communication Services.

        This method uses a predefined HTML email template and subject based on the given type,
        formats the content with the provided body token and host URL, and sends the email
        through Azure Communication Services.

        Args:
            to_email (str): The recipient's email address.
            body (str): The dynamic token or value to inject into the email template.
            type (str): The type of email to send, which determines the subject and template
                        (e.g., 'reset_password', 'verify_org', 'approved_registration').

        Raises:
            Exception: If the email fails to send via Azure Communication Services.
        """
        template, subject = self.template_map.get(type).values()

        message = {
            "senderAddress": self.config.get('sender_email'),
            "content": {
                "subject": subject,
                "html": template.format(token=body, host=os.getenv("TRUMPET_CLOUD_WEBSITE_HOST"))
            },
            "recipients": {
                "to": [{"address": to_email }]
            }
        }

        email_client = EmailClient.from_connection_string(self.config.get('azure_connection_string'))
        try:
            email_client.begin_send(message)
        except Exception as e:
            raise Exception(f"Failed to initiate email send via Azure: {str(e)}")

