import asyncio
import logging
import pytest

from email.message import EmailMessage
from typing import List
from abc import ABC, abstractmethod

from aiosmtpd.controller import Controller
from aiosmtpd.handlers import AsyncMessage
from aiosmtpd.controller import Controller
from aiosmtpd.smtp import Envelope
from email.message import EmailMessage


class EmailSender(ABC):
    @abstractmethod
    def send_email(self, to: List[str], subject: str, body: str, from_email: str) -> None:
        pass


class EmailService:
    def __init__(self, email_sender: EmailSender):
        self.email_sender = email_sender

    def send(self, to: List[str], subject: str, body: str, from_email: str) -> None:
        """Delegates the email sending to the strategy provided."""
        self.email_sender.send_email(to, subject, body, from_email)


class SmtpEmailSender(EmailSender):
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, use_tls: bool = True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls

    async def send_email(self, to: List[str], subject: str, body: str, from_email: str) -> None:
        # Create an EmailMessage object
        message = EmailMessage()
        message['From'] = from_email
        message['To'] = ", ".join(to)
        message['Subject'] = subject
        message.set_content(body)

        try:
            # Asynchronously send the email using aiosmtplib
            await send(
                message,
                hostname=self.smtp_server,
                port=self.smtp_port,
                username=self.username,
                password=self.password,
                use_tls=self.use_tls,
            )

            logging.info("Email sent successfully to %s", to)

        except Exception as e:
            logging.error("Failed to send email to %s: %s", to, str(e))
            raise e  # Re-raise the exception after logging


"""implementation
class SimpleHandler(AsyncMessage):
    async def handle_message(self, message: EmailMessage):
        # Process incoming email here
        logging.info("Received message from %s", message['From'])
        # You can add processing logic here or forward the email using your SmtpEmailSender
        print("Subject:", message['Subject'])
        print("Body:", message.get_content())


async def main():
    handler = SimpleHandler()
    controller = Controller(handler, hostname='localhost', port=8025)
    controller.start()

    try:
        smtp_sender = SmtpEmailSender(
            smtp_server='smtp.example.com',
            smtp_port=587,
            username='your_username',
            password='your_password',
            use_tls=True
        )

        email_service = EmailService(smtp_sender)
        await email_service.send(
            to=['recipient@example.com'],
            subject='Test Email',
            body='This is a test email sent using aiosmtplib.',
            from_email='sender@example.com'
        )
    finally:
        controller.stop()

# Run the asyncio loop
asyncio.run(main())
"""


class MockSMTPHandler:
    def __init__(self):
        self.emails = []

    async def handle_DATA(self, server, session, envelope: Envelope):
        # Store the envelope data for later inspection
        self.emails.append(envelope)
        return '250 Message accepted for delivery'


@pytest.fixture
def smtp_server():
    handler = MockSMTPHandler()
    controller = Controller(handler, hostname='localhost', port=8025)
    controller.start()

    yield handler

    controller.stop()


@pytest.fixture
def smtp_email_sender():
    return SmtpEmailSender(
        smtp_server='localhost',
        smtp_port=8025,
        username='',
        password='',
        use_tls=False
    )


@pytest.fixture
def email_service(smtp_email_sender):
    return EmailService(smtp_email_sender)


@pytest.mark.asyncio
class TestEmailService:
    async def test_send_email_with_mock_server(
        self,
        smtp_server: MockSMTPHandler,
        smtp_email_sender: SmtpEmailSender
    ) -> None:
        await smtp_email_sender.send_email(
            to=['recipient@test.com'],
            subject='Test Subject',
            body='Test Body',
            from_email='sender@test.com'
        )

        assert len(smtp_server.emails) == 1

        email = smtp_server.emails[0]
        assert email.mail_from == 'sender@test.com'
        assert email.rcpt_tos == ['recipient@test.com']
        assert 'Test Subject' in email.content.decode()
        assert 'Test Body' in email.content.decode()

    async def test_email_service_with_mock_server(
        self,
        smtp_server: MockSMTPHandler,
        email_service: EmailService
    ) -> None:
        await email_service.send(
            to=['recipient@test.com'],
            subject='Integration Test',
            body='Testing Email Service integration with SMTP',
            from_email='sender@test.com'
        )

        assert len(smtp_server.emails) == 1

        email = smtp_server.emails[0]
        assert email.mail_from == 'sender@test.com'
        assert email.rcpt_tos == ['recipient@test.com']
        assert 'Integration Test' in email.content.decode()
        assert 'Testing Email Service integration with SMTP' in email.content.decode()
