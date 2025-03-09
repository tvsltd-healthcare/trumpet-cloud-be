from typing import Dict

from adapters.auth_adapters.jwt_adapter import JWTAdapter
from application_layer.abstractions.auth_interface import IAuthenticationHandler


class TokenHandlerFactory:
    """
    Token handler factory class
    """
    @staticmethod
    def select_adapter(adapter: Dict) -> IAuthenticationHandler:
        """
        Select an authentication handler
        Args:
            adapter: String representation of the authentication adapter

        Returns:
            IAuthenticationHandler

        """
        handler_type = adapter.get('type')

        match handler_type:
            case 'JWT':
                return JWTAdapter(adapter.get('jwt'))
            case _:
                raise ValueError(f'Unsupported adapter type: {adapter}')
