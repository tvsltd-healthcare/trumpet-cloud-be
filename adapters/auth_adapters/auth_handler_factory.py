from typing import Dict

from adapters.auth_adapters.jwt_adapter import JWTAdapter
from application_layer.abstractions.auth_interface import IAuthenticationHandler


class AuthHandlerFactory:
    """
    Token handler factory class
    """
    @staticmethod
    def get_handler(config: Dict) -> IAuthenticationHandler:
        """
        Select an authentication handler
        Args:
            config: String representation of the authentication adapter

        Returns:
            IAuthenticationHandler

        """
        handler_type = config.get('type')

        match handler_type:
            case 'JWT':
                return JWTAdapter(config.get('jwt'))
            case _:
                raise ValueError(f'Unsupported adapter type: {config}')
