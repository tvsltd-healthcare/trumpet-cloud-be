from typing import Dict

import pytest


def send_registration_disapproval_email(to_address: str, from_address: str) -> Dict[str, str]:
    """
    Function id: 43
    Function to send registration disapproval email to researcher.

    Parameters:
        to_address (str): Email address of the researcher
        from_address (str): Researcher server email address

    Return:
        Dict[str, str]: A dictionary containing email components:
            -'from': Researcher server email address
            -'to': Email address of the researcher
            -'subject': Subject of the email
            -'body': Body of the email    
    """

    body = "We are sorry. Your registration has not been approved. Please verify your documents and try again."
    subject = "Registration Not Approved."

    return {
        "from": from_address,
        "to": to_address,
        "subject": subject,
        "body": body
    }


@pytest.fixture
def email_data():
    return {
        "to_address": "researcher@example.com",
        "from_address": "no-reply@example.com",
    }


@pytest.fixture
def email_template(email_data):
    return send_registration_disapproval_email(
        email_data['to_address'],
        email_data['from_address']
    )


class TestSendRegistrationDisapprovalEmail:
    def test_disapproval_email_from_address(self, email_template, email_data):
        assert email_template["from"] == email_data["from_address"], "The 'from' address is incorrect."

    def test_disapproval_email_to_address(self, email_template, email_data):
        assert email_template["to"] == email_data["to_address"], "The 'to' address is incorrect."

    def test_disapproval_email_subject(self, email_template):
        assert email_template["subject"] == "Registration Not Approved.", "The 'subject' is correct."

    def test_disapproval_email_body(self, email_template):
        assert email_template["body"] == "We are sorry. Your registration has not been approved. Please verify your documents and try again.", "The 'body' is correct."
