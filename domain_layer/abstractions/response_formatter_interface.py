from abc import ABC, abstractmethod
from typing import Any, Dict


class IResponseFormatter(ABC):
    """Interface for formatting REST API responses.

    Provides a standard structure for success, error, and validation error responses.
    """

    @abstractmethod
    def success(self, data: Any, message: str, status_code: int = 200) -> Dict[str, Any]:
        """Format a successful API response.

        Args:
            data: The payload to be returned in the response.
            message: A short message describing the response.
            status_code: HTTP status code (default is 200).

        Returns:
            A dictionary containing the formatted success response.
        """
        pass

    @abstractmethod
    def error(self, message: str, status_code: int = 500) -> Dict[str, Any]:
        """Format a generic error API response.

        Args:
            message: A description of the error.
            status_code: HTTP status code (default is 500).

        Returns:
            A dictionary containing the formatted error response.
        """
        pass

    @abstractmethod
    def validation_error(self, errors: Any, message: str, status_code: int = 422) -> Dict[str, Any]:
        """Format a validation error API response.

        Args:
            errors: A dictionary or list describing validation issues.
            message: A message indicating the validation failure.
            status_code: HTTP status code (default is 422).

        Returns:
            A dictionary containing the formatted validation error response.
        """
        pass
