from fastapi import Request
from adapters.auth_adapters.auth_handler import AuthHandler


def auth_dispatch(request: Request) -> None:
    print("tesss")
    print(request.headers)
    token = AuthHandler.generate_token({"user_id": 1})
    print(token)
    # validate_token = AuthHandler.validate_token(token)
    # print(validate_token)
