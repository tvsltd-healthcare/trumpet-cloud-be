import re
import pytest

from typing import Dict


def generate_researcher_signup_varification_email(signup_token: str, from_email: str, to_email: str) -> Dict[str, str]:
    """
    function id - 111
    Generates an email for researcher signup verification.

    Args:
        signup_token (str): The signup token that will be used to generate the signup link.
        from_email (str): The sender's email address.
        to_email (str): The recipient's email address.

    Returns:
        Dict[str, str]: A dictionary containing the email components:
            - 'from': The sender's email address.
            - 'to': The recipient's email address.
            - 'body': The email content, which includes the signup link.
    """

    signup_link = f"https://example.com/signup/token/{signup_token}"
    body = f"Please click on the following link to verify your email and complete your signup: {signup_link}"
    subject = "Invitation for collaboration as a Researcher"
    
    return {
        "from": from_email,
        "to": to_email,
        "subject": subject,
        "body": body
    }
    

@pytest.fixture
def email_params():
    return {
        "signup_token": "testToken123",
        "to_email": "researcher@example.com",
        "from_email": "no-reply@example.com"
    }

@pytest.fixture
def generated_email(email_params):
    return generate_researcher_signup_varification_email(
        email_params["signup_token"], 
        email_params["from_email"], 
        email_params["to_email"]
    )

class TestGenerateResearcherVarificationEmail:
    def test_generate_researcher_varification_email_from(self, generated_email, email_params):
        assert generated_email["from"] == email_params["from_email"], "The 'from' email does not match the expected value."

    def test_generate_researcher_signup_varification_email_to(self, generated_email, email_params):
        assert generated_email["to"] == email_params["to_email"], "The 'to' email does not match the expected value."

    def test_generate_researcher_signup_varification_email_subject(self, generated_email, email_params):
        assert generated_email["subject"] == "Invitation for collaboration as a Researcher", "The 'subject' of the email does not match the expected value."

    def test_generate_researcher_signup_varification_email_body_contains_link(self, generated_email, email_params):
        url_pattern = fr'(https?://[^\s]+{email_params["signup_token"]})'
        assert re.search(url_pattern, generated_email["body"]), "The email body does not contain a valid URL with token."
        
   