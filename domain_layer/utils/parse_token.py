from domain_layer.auth_manager import AuthManager

def token_parser(token: str) -> str:
    """
    Parses and validates a Bearer JWT token, returning the decoded data.
    This function:
    1. Strips the "Bearer " prefix from the token string.
    2. Uses the `AuthManager` to decode and validate the token.
    3. Returns the decoded token data.
    Args:
        token (str): The JWT token string prefixed with "Bearer ".
    Returns:
        dict: Decoded data extracted from the token (e.g., user email, roles, etc.).
    Raises:
        ValueError: If the token is missing, empty, or invalid.
        RuntimeError: If token decoding or validation fails.
    Example:
        ```python
        token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        decoded = token_parser(token)
        # Returns something like: {"email": "user@example.com", "exp": 1234567890}
        ```
    """
    try:
        token = token.replace("Bearer ", "").strip()
        auth_getter_adapter = AuthManager.get()
        parse_token = auth_getter_adapter.read_data(token)

        if not parse_token:
            raise ValueError("Missing valid authorization header.")
        return parse_token

    except ValueError as ve:
        raise ValueError(f"Validation error: {str(ve)}")
    except RuntimeError as re:
        raise RuntimeError(f"Token processing failed: {str(re)}")
    except AttributeError as ae:
        raise AttributeError(f"Invalid attribute access: {str(ae)}")
    except Exception as e:
        raise ValueError(f"Token parsing failed: {str(e)}")