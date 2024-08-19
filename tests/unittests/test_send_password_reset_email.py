from typing import Dict
import re
import pytest


def send_password_reset_email(to_address: str, from_address: str, reset_token: str) -> Dict[str, str]:
    """
    Function id: 135
    Function to send password reset email to a Researcher.

    Parameters:
        to_address (str): Email address of the Researcher
        from_address (str): Server email address
        reset_token (str): The reset token to be included in the reset link

    Return:
        Dict[str, str]: A dictionary containing email components:
            -'from': Server email address
            -'to': Email address of the Researcher
            -'subject': Subject of the email
            -'body': Body of the email    
    """

    reset_link = f"https://example.com/reset/token/{reset_token}"
    body = f"You requested a password reset. Click the link below to reset your password:\n{reset_link}"
    subject = "Password Reset Request."

    return {
        "from": from_address,
        "to": to_address,
        "subject": subject,
        "body": body
    }


@pytest.fixture
def password_reset_email_data():
    return {
        "to_address": "user@example.com",
        "from_address": "no-reply@example.com",
        "reset_token": "abc123xyz"
    }


@pytest.fixture
def password_reset_email_template(password_reset_email_data):
    return send_password_reset_email(
        password_reset_email_data['to_address'],
        password_reset_email_data['from_address'],
        password_reset_email_data['reset_token']
    )


class TestSendPasswordResetEmail:
    def test_password_reset_email_from_address(self, password_reset_email_template, password_reset_email_data):
        assert password_reset_email_template["from"] == password_reset_email_data["from_address"], "The 'from' address is incorrect."

    def test_password_reset_email_to_address(self, password_reset_email_template, password_reset_email_data):
        assert password_reset_email_template["to"] == password_reset_email_data["to_address"], "The 'to' address is incorrect."

    def test_password_reset_email_subject(self, password_reset_email_template):
        assert password_reset_email_template["subject"] == "Password Reset Request.", "The 'subject' is incorrect."

    def test_password_reset_email_body_contains_reset_link(self, password_reset_email_template, password_reset_email_data):
        reset_link_pattern = re.compile(r"https://example.com/reset/token/[a-zA-Z0-9]+")
        assert re.search(reset_link_pattern, password_reset_email_template["body"]), "The 'reset_token' is missing in the body."

    def test_password_reset_email_body_contains_correct_token(self, password_reset_email_template, password_reset_email_data):
        expected_reset_link = f"https://example.com/reset/token/{password_reset_email_data['reset_token']}"
        assert expected_reset_link in password_reset_email_template["body"], "The 'reset_token' in the body is incorrect."
