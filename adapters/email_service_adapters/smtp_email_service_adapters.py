from domain_layer.abstractions.email_sending_interface import IEmailService
from email_service.smtp_email_service import SmtpEmailService


class EmailServiceAdapter(IEmailService):

    def __init__(self, email_service: SmtpEmailService):
        self.email_service = email_service
    
    def send_email(self, to_email: str, body: str ) -> None:
        self.email_service.send_email(to_email, body )
        
