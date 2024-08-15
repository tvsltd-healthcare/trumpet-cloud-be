import pytest

from datetime import datetime, timedelta

researcher_email_verification_token_validity_period_in_hours = 72

def is_researcher_email_verification_token_expired(stored_token_created_at: datetime) -> bool:
    """
    function id - 112
    Checks if a researcher's email verification token is expired based on its creation time.

    Args:
        stored_token_created_at (datetime): The date and time when the token was created.

    Returns:
        bool: True if the token is expired, False if the token is still valid.
    """

    # Define the expiration threshold
    expiration_threshold = timedelta(hours=researcher_email_verification_token_validity_period_in_hours)
    current_time = datetime.now()
    
    # Check if the token is expired
    if current_time - stored_token_created_at > expiration_threshold:
        return 1  # Token is expired
    
    return 0  # Token is valid
    

class TestIsResearcherEmailVerificationTokenExpired(object):
    def test_is_researcher_email_veridfication_token_not_expired(self):
        stored_token_created_at = datetime.now() - timedelta(hours=71)  # Token created 71 hours ago
        result = is_researcher_email_verification_token_expired(stored_token_created_at)
        assert result == False, "The token should be valid (not expired) but returned expired."

    def test_is_researcher_email_verification_token_expired(self):
        stored_token_created_at = datetime.now() - timedelta(hours=73)  # Token created 73 hours ago
        result = is_researcher_email_verification_token_expired(stored_token_created_at)
        assert result == True, "The token should be expired but returned valid."
