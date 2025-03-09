from abc import ABC, abstractmethod
from typing import Dict


class IAuthenticationHandler(ABC):
    """
    Interface for all authentication handlers.
    """

    @abstractmethod
    def generate_token(self, params: Dict) -> Dict:
        """
        Interface for Generate token
        Args:
            params: Dictionary of parameters
        Returns:
            Dict: Dictionary containing token, refresh token and other information
        """
        pass

    @abstractmethod
    def validate_token(self, token: str) -> bool:
        """
        Interface for Validate token
        Args:
            token: Authentication token
        Returns:
            bool: True if token is valid, False otherwise
        """
        pass

    @abstractmethod
    def generate_refresh_token(self, params: Dict) -> Dict:
        """
        Interface for Refresh token
        Args:
            params: Parameters for Refresh token
        Returns:
            Dict: Dictionary containing token, refresh token and other information

        """
        pass

    @abstractmethod
    def validate_refresh_token(self, refresh_token: str) -> bool:
        """
        Interface for Validate refresh token
        Args:
            refresh_token:

        Returns:
            bool: True if refresh token is valid, False otherwise

        """
        pass

    @abstractmethod
    def read_data(self, token: str) -> Dict[str, str]:
        """
        Interface for Read data from token
        Args:
            token:

        Returns:
            Dict: Dictionary containing user information get from token

        """
        pass


