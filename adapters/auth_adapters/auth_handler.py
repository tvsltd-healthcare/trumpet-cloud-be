from typing import Dict

from application_layer.abstractions.auth_interface import IAuthenticationHandler
from wrap_auth.entrypoint import AuthWrapper

JWT_config = {
    "secret": "my_secret_key",
    "algorithm": "HS256",
    "expiry": 3600,
}


class AuthHandler(IAuthenticationHandler):

    def generate_token(self, params: Dict) -> str:
        jwt_handler = AuthWrapper.auth_handler("JWT", JWT_config)
        print(jwt_handler)
        # Generate a JWT Token
        jwt_token = jwt_handler.generate_token(params)
        print(f"Generated JWT Token: {jwt_token}")
        return jwt_token

    def validate_token(self, token: str) -> bool:
        jwt_handler = AuthWrapper.auth_handler("JWT", JWT_config)
        validated_token = jwt_handler.validate_token(token)
        print(f"Validated JWT Token: {validated_token}")
        return validated_token
