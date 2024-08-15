import pytest

from datetime import datetime, timedelta

password_reset_token_validity_period_in_hours = 72

def is_researcher_password_reset_token_expired(stored_token_created_at: datetime) -> bool:
    """
    function id - 69
    Checks if a researcher's password reset token is expired based on its creation time.

    Args:
        stored_token_created_at (datetime): The date and time when the token was created.

    Returns:
        bool: True if the token is expired, False if the token is still valid.
    """

    # Define the expiration threshold
    expiration_threshold = timedelta(hours=password_reset_token_validity_period_in_hours)
    current_time = datetime.now()
    
    # Check if the token is expired
    if current_time - stored_token_created_at > expiration_threshold:
        return 1  # Token is expired
    
    return 0  # Token is valid
    

class TestValidateResearcherPasswordResetToken(object):
    def test_is_researcher_password_reset_token_not_expired(self):
        stored_token_created_at = datetime.now() - timedelta(hours=71)  # Token created 71 hours ago
        result = is_researcher_password_reset_token_expired(stored_token_created_at)
        assert result == False, "The token should be valid (not expired) but returned expired."

    def test_is_researcher_password_reset_token_expired(self):
        stored_token_created_at = datetime.now() - timedelta(hours=73)  # Token created 73 hours ago
        result = is_researcher_password_reset_token_expired(stored_token_created_at)
        assert result == True, "The token should be expired but returned valid."
        
   