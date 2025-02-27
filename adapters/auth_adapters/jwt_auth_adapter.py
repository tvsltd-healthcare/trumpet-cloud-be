import os
from typing import Dict

from application_layer.abstractions.auth_interface import IAuthenticationHandler
from wrap_auth.entrypoint import AuthWrapper

JWT_config = {
    "secret": os.getenv("JWT_SECRET"),
    "algorithm": os.getenv("JWT_ALGORITHM"),
    "expiry": os.getenv("JWT_EXPIRY"),
}
jwt_handler = AuthWrapper.auth_handler("JWT", JWT_config)


class JWTAuthAdapter(IAuthenticationHandler):
    def generate_token(self, params: Dict) -> str:
        jwt_token = jwt_handler.generate_token(params)
        return jwt_token

    def validate_token(self, token: str) -> bool:
        validated_token = jwt_handler.validate_token(token)
        return validated_token

    def read_data(self, token: str) -> Dict:
        jwt_data = jwt_handler.read_data(token)
        return jwt_data
