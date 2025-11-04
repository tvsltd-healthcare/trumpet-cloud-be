import re
from typing import Union

def is_strong_password(password: str) -> Union[bool, str]:
    """
    Validates the strength of a password based on the following criteria:
        - Minimum length of 6 characters
        - At least one lowercase letter
        - At least one uppercase letter
        - At least one digit

    Args:
        password (str): The password string to validate.

    Returns:
        Union[bool, str]:
            - True if the password meets all strength requirements.
            - A string message describing the specific validation failure otherwise.
    """
    if len(password) < 6:
        return "Password must be at least 6 characters long."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter (a–z)."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter (A–Z)."
    if not re.search(r"[0-9]", password):
        return "Password must contain at least one numeric digit (0–9)."
    return True
