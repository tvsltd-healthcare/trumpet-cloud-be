import re
import os

from typing import Dict, Optional

from jinja2 import Template


file_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Read the Jinja2 email template
with open(os.path.join(file_path, "tests", "email_content.html"), "r") as file:
    template_str = file.read()

email_template = Template(template_str)


class TestGenerateVerificationEmailContent:
    subject = "Verify your registration email"
    from_email = "no-reply@system-domain.aa"
    verification_link = "https://example.com/verify?token=c9ec9cc7-a549-4e4f-a50c-1bacb48c2223"

    def test_email_subject(self) -> None:
        """Test that the email subject is 'Verify your registration email'."""
        email_content = generate_verification_email_content(subject=self.subject, 
                                                            verification_link=self.verification_link, 
                                                            from_email=self.from_email)

        assert str.lower(email_content['subject']) == "verify your registration email"

    def test_email_body_contains_verification_link(self) -> None:
        """Test that the email body contains the verification link."""
        email_content = generate_verification_email_content(subject=self.subject, 
                                                            verification_link=self.verification_link, 
                                                            from_email=self.from_email)

        email_body = email_content['body']
        
        # find for the UUID4 or randomly generated token
        url_pattern = r"https://[\w.-]+/verify\?token=[\w-]+"
        matches = re.findall(url_pattern, email_body)
        
        assert self.verification_link in matches

    def test_email_from_address(self) -> None:
        """Test that the email from address is 'no-reply@system-domain.aa'."""
        email_content = generate_verification_email_content(subject=self.subject, 
                                                            verification_link=self.verification_link, 
                                                            from_email=self.from_email)
        
        from_email_address = email_content['from_email']

        assert from_email_address == "no-reply@system-domain.aa"
        assert str.lower(from_email_address.split('@')[0]) == "no-reply"


def generate_verification_email_content(subject: str, verification_link: str, from_email: str, 
                                        user_name: Optional[str] = "Onboard!") -> Dict[str, str]:
    """Generates the content of the verification email."""
    body = email_template.render(user_name=user_name, verification_link=verification_link)

    return {
        "subject": subject,
        "from_email": from_email,
        "body": body
    }
