from abc import ABC, abstractmethod

class IEmailService(ABC):
    @abstractmethod
    def send_email(self, to_email: str, subject: str, body: str, from_email: str) -> None:
        """Send an email to the specified recipient."""
        pass