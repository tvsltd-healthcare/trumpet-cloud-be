import re
import pytest

from typing import Dict


def generate_researcher_signup_varification_email(signup_link: str, from_email: str, to_email: str) -> Dict[str, str]:
    """
    function id - 111
    Generates an email for researcher verification.

    Args:
        signup_link (str): The signup link to be included in the email body.
        from_email (str): The sender's email address.
        to_email (str): The recipient's email address.

    Returns:
        Dict[str, str]: A dictionary containing the email components:
            - 'from': The sender's email address.
            - 'to': The recipient's email address.
            - 'body': The email content, which includes the signup link.
    """

    body = f"Please click on the following link to verify your email and complete your signup: {signup_link}"
    
    return {
        "from": from_email,
        "to": to_email,
        "body": body
    }
    

@pytest.fixture
def email_params():
    signup_link = "https://example.com/signup"
    to_email = "researcher@example.com"
    from_email = "no-reply@example.com"
    return signup_link, to_email, from_email

class TestGenerateResearcherVarificationEmail:
    def test_generate_researcher_varification_email_from(self, email_params):
        signup_link, to_email, from_email = email_params
        result = generate_researcher_signup_varification_email(signup_link, from_email, to_email)
        assert result["from"] == from_email, "The 'from' email does not match the expected value."

    def test_generate_researcher_signup_varification_email_to(self, email_params):
        signup_link, to_email, from_email = email_params
        result = generate_researcher_signup_varification_email(signup_link, from_email, to_email)
        assert result["to"] == to_email, "The 'to' email does not match the expected value."

    def test_generate_researcher_signup_varification_email_body_contains_link(self, email_params):
        signup_link, to_email, from_email = email_params
        result = generate_researcher_signup_varification_email(signup_link, from_email, to_email)
        url_pattern = r'(https?://[^\s]+)'
        assert re.search(url_pattern, result["body"]), "The email body does not contain a valid URL."
        
   