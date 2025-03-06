import os

from fastapi import Request, HTTPException
from starlette import status

from adapters.auth_adapters.token_handler_factory import TokenHandlerFactory

config = {
    "type": "JWT"
}


def auth_dispatch(request: Request) -> None:
    authorization = request.headers.get("Authorization")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    token = authorization.split("Bearer ")[1]
    auth_factory = TokenHandlerFactory.select_adapter(config)
    check_token = auth_factory.validate_token(token)
    if check_token:
        read_token_data = auth_factory.read_data(token)
        request.state.user_id = read_token_data["user_id"]
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
