from domain_layer.abstractions.email_sending_interface import IEmailService
from email_service.azure_email_service import AzureEmailService


class AzureEmailServiceAdapter(IEmailService):

    def __init__(self, email_service: AzureEmailService):
        self.email_service = email_service

    def send_email(self, to_email: str, body: str, type: str) -> None:
        self.email_service.send_email(to_email, body, type)
