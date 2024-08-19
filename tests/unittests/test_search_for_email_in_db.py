import pytest

"""
Function Id: 127
Function to search for email in database
"""


def is_email_match(input_email: str, db_email: str) -> bool:
    """
    Check if the input email matches the database email.

    Parameters:
        input_email (str): The email provided by the user.
        db_email (str): The database email.

    Returns:
        bool: True if the emails match, False otherwise.
    """
    return input_email.lower() == db_email.lower()


# Fixtures for testing
@pytest.fixture
def db_email():
    return "user@example.com"


@pytest.fixture
def matching_email():
    return "user@example.com"


@pytest.fixture
def non_matching_email():
    return "different@example.com"


@pytest.fixture
def case_insensitive_email():
    return "User@Example.Com"


# Test cases
class TestEmailMatch:
    def test_emails_match(self, matching_email, db_email):
        assert is_email_match(matching_email, db_email) is True, "Emails should match."

    def test_emails_do_not_match(self, non_matching_email, db_email):
        assert is_email_match(non_matching_email, db_email) is False, "Emails should not match."

    def test_case_insensitive_match(self, case_insensitive_email, db_email):
        assert is_email_match(case_insensitive_email, db_email) is True, "Emails should match (case-insensitive)."
