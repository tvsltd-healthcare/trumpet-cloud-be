from enum import Enum
from typing import Dict

from adapters.email_service_adapters.azure_email_service_adapters import AzureEmailServiceAdapter
from adapters.email_service_adapters.smtp_email_service_adapters import SMTPEmailServiceAdapter
from domain_layer.abstractions.email_sending_interface import IEmailService
from email_service.azure_email_service import AzureEmailService
from email_service.smtp_email_service import SmtpEmailService


class EmailServiceType(Enum):
    """Supported email service types."""
    SMTP = "SMTP"
    AZURE = "AZURE"


class EmailServiceHandlerFactory:
    """
    Token handler factory class
    """

    @staticmethod
    def get_handler(config: Dict) -> IEmailService:
        """
        Select an authentication handler
        Args:
            config: String representation of the authentication adapter

        Returns:
            IAuthenticationHandler

        """

        match config.get('name'):
            case EmailServiceType.SMTP.value:
                return SMTPEmailServiceAdapter(SmtpEmailService(config.get('config')))
            case EmailServiceType.AZURE.value:
                return AzureEmailServiceAdapter(AzureEmailService(config.get('config')))
            case _:
                raise ValueError(f'Unsupported adapter type: {config}')
