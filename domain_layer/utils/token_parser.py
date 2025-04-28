from domain_layer.auth_manager import AuthManager
from domain_layer.response_formatter import ResponseFormatter

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
        str: Decoded data extracted from the token (e.g., user email, roles, etc.).
    Raises:
        ValueError: If the token is missing, invalid, or decoding fails.
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

        if token:
            return parse_token
        else: 
            return ResponseFormatter.error('Missing valid authorization header.', 400)

    except Exception as e:
        return ResponseFormatter.error(str(e), 500)
