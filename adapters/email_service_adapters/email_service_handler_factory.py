from enum import Enum
import os
from typing import Dict
from adapters.email_service_adapters.azure_email_service_adapters import AzureEmailServiceAdapter
from email_service.azure_email_service import AzureEmailService
from email_service.smtp_email_service import SmtpEmailService
from domain_layer.abstractions.email_sending_interface import IEmailService
from adapters.email_service_adapters.smtp_email_service_adapters import SMTPEmailServiceAdapter

class EmailServiceType(Enum):
    """Supported email service types."""
    SMTP = "SMTP"
    AZURE = "AZURE"
    ACTIVE_EMAIL_SERVICE_NAME = os.getenv("EMAIL_SERVICE_TYPE")

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
        handler_type = config.get('name')

        match handler_type:
            case EmailServiceType.SMTP:
                return SMTPEmailServiceAdapter(SmtpEmailService(config.get('config')))
            case EmailServiceType.AZURE:
                return AzureEmailServiceAdapter(AzureEmailService(config.get('config')))
            case _:
                raise ValueError(f'Unsupported adapter type: {config}')
