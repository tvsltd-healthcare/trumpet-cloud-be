from typing import Any, Dict

from domain_layer.abstractions.response_formatter_interface import IResponseFormatter


class ResponseFormatter(IResponseFormatter):
    """Concrete implementation of IResponseFormatter for formatting REST API responses.

    This class provides a standard response format for successful requests,
    generic errors, and validation-related errors.
    """

    def success(self, data: Any, message: str, status_code: int = 200) -> Dict[str, Any]:
        """Format a successful API response.

        Args:
            data: The payload to be returned in the response.
            message: A short message describing the response.
            status_code: HTTP status code (default is 200).

        Returns:
            Dict[str, Any]: A dictionary containing the formatted success response.
        """
        return {
            "status_code": status_code,
            "message": message,
            "data": data
        }

    def error(self, message: str, status_code: int = 500) -> Dict[str, Any]:
        """Format a generic error API response.

        Args:
            message: A description of the error.
            status_code: HTTP status code (default is 500).

        Returns:
            Dict[str, Any]: A dictionary containing the formatted error response.
        """
        return {
            "status_code": status_code,
            "message": message
        }

    def validation_error(self, errors: Any, message: str, status_code: int = 422) -> Dict[str, Any]:
        """Format a validation error API response.

        Args:
            errors: A dictionary or list describing validation issues.
            message: A message indicating the validation failure.
            status_code: HTTP status code (default is 422).

        Returns:
            Dict[str, Any]: A dictionary containing the formatted validation error response.
        """
        return {
            "status_code": status_code,
            "message": message,
            "errors": errors
        }
