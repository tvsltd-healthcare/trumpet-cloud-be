import os
from abc import ABC
from typing import Dict

from application_layer.abstractions.auth_interface import IAuthenticationHandler
from wrap_auth.entrypoint import AuthWrapper
"""
config for JWT adapter
"""
config = {
    "secret": os.getenv("JWT_SECRET"),
    "algorithm": os.getenv("JWT_ALGORITHM"),
    "expiry": os.getenv("JWT_EXPIRY"),

}
jwt = AuthWrapper.auth_handler("JWT", config)


class JWTAdapter(IAuthenticationHandler):
    """
    JWT adapter
    """
    def generate_token(self, params: Dict) -> Dict:
        """
        Function to generate JWT token
        Args:
            params: Dictionary containing JWT config with parameters

        Returns:
            Dict containing JWT token

        """
        return jwt.generate_token(params)

    def validate_token(self, token: str) -> bool:
        """
        Function to validate JWT token
        Args:
            token: JWT token

        Returns:
            True if token is valid, False otherwise

        """
        return jwt.validate_token(token)

    def generate_refresh_token(self, params: Dict) -> Dict:
        """
        Function to generate refresh token
        Args:
            params: Function containing JWT config with parameters

        Returns:
            Dict containing refresh token

        """
        return jwt.generate_refresh_token(params)

    def validate_refresh_token(self, token: str) -> bool:
        """
        Function to validate refresh token
        Args:
            token: JWT token

        Returns:
            True if token is valid, False otherwise

        """
        return jwt.validate_refresh_token(token)

    def read_data(self, token: str) -> Dict[str, str]:
        """
        Function to read data from JWT token
        Args:
            token: Token JWT

        Returns:
            Dict containing data from JWT token

        """
        return jwt.read_data(token)
