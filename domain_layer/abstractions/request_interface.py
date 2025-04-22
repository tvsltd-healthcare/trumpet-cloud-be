from typing import Protocol, runtime_checkable


@runtime_checkable
class IRequest(Protocol):
    """
    Interface for a response handler to generate structured JSON API responses.
    """

    def get_json(self) -> dict:
        """Return the request body parsed as JSON (or an empty dict)."""
        pass

    def get_body(self) -> bytes:
        """Return the request body as bytes (or an empty bytes object)."""
        pass

    def get_query_params(self) -> dict:
        """Return the query parameters as a dictionary."""
        pass

    def get_path_params(self) -> dict:
        """Return the path parameters as a dictionary."""
        pass

    def get_headers(self) -> dict:
        """Return the request headers as a dictionary."""
        pass

    def get_cookies(self) -> dict:
        """Return the cookies as a dictionary."""
        pass

    def get_url(self) -> str:
        """Return the request URL as a string."""
        pass

    def get_form_data(self) -> dict:
        """Return the uploaded files"""
        pass
