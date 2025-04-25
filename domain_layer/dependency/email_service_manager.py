from domain_layer.abstractions.email_sending_interface import IEmailService

class EmailServiceManager:
    
    @classmethod
    def set(cls, instance: IEmailService):
         cls.instance = instance

    @classmethod
    def get(cls) -> IEmailService:
        return cls.instance
