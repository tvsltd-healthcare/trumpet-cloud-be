import os
from abc import ABC
from typing import Dict

from application_layer.abstractions.auth_interface import IAuthenticationHandler
from wrap_auth.entrypoint import AuthWrapper


class JWTAdapter(IAuthenticationHandler):
    """
       JWT adapter to handle JWT-related operations like generating and validating tokens
    """
    def __init__(self, config: Dict):
        """
            Initialize the JWT Adapter with the provided configuration

            Args:
                config: Dictionary containing JWT-related configurations like secret, algorithm, etc.
        """
        self.config = config
        self.jwt = AuthWrapper.auth_handler("JWT", self.config)

    def generate_token(self, params: Dict) -> Dict:
        """
        Function to generate JWT token
        Args:
            params: Dictionary containing JWT config with parameters

        Returns:
            Dict containing JWT token

        """
        return self.jwt.generate_token(params)

    def validate_token(self, token: str) -> bool:
        """
        Function to validate JWT token
        Args:
            token: JWT token

        Returns:
            True if token is valid, False otherwise

        """
        return self.jwt.validate_token(token)

    def generate_refresh_token(self, params: Dict) -> Dict:
        """
        Function to generate refresh token
        Args:
            params: Function containing JWT config with parameters

        Returns:
            Dict containing refresh token

        """
        return self.jwt.generate_refresh_token(params)

    def validate_refresh_token(self, token: str) -> bool:
        """
        Function to validate refresh token
        Args:
            token: JWT token

        Returns:
            True if token is valid, False otherwise

        """
        return self.jwt.validate_refresh_token(token)

    def read_data(self, token: str) -> Dict[str, str]:
        """
        Function to read data from JWT token
        Args:
            token: Token JWT

        Returns:
            Dict containing data from JWT token

        """
        return self.jwt.read_data(token)

    def check_token_expiry(self, token: str) -> bool:
        """
        Function to check if JWT token is expired
        Args:
            token: JWT token

        Returns:
            True if token is expired, False otherwise

        """
        return self.jwt.check_token_expiry(token)
