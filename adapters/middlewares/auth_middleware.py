from fastapi import Request, HTTPException
from starlette import status

from adapters.auth_adapters.jwt_auth_adapter import JWTAuthAdapter


def auth_dispatch(request: Request) -> None:
    auth_handler = JWTAuthAdapter()
    check_token = auth_handler.validate_token(request.headers["token"])
    if check_token:
        read_token_data = auth_handler.read_data(request.headers["token"])
        request.state.user_id = read_token_data["user_id"]
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

