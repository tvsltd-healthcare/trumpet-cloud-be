from typing import Dict
from adapters.email_service_adapters.smtp_email_service_adapters import SMTPEmailServiceAdapter
from domain_layer.abstractions.email_sending_interface import IEmailService
from email_service.smtp_email_service import SmtpEmailService


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
            case 'SMTP':
                return SMTPEmailServiceAdapter(SmtpEmailService(config.get('config')))
            case _:
                raise ValueError(f'Unsupported adapter type: {config}')
