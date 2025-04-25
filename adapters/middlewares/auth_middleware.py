import os
from typing import Dict

from fastapi import Request, HTTPException
from starlette import status

from adapters.auth_adapters.auth_handler_factory import AuthHandlerFactory


class AuthMiddleware:
    """
        AuthMiddleware class to handle JWT authentication logic
    """

    def __init__(self, auth_handler):
        """
            Initializes the middleware with the authentication configuration.

            Args:
                auth_config: Configuration dictionary to set up JWT and other auth types
        """
        self.auth_handler = auth_handler

    def __call__(self, request: Request):
        """
           Middleware execution logic, checks for Authorization token and validates it based on the selected auth adapter (JWT).

           Args:
               request: The incoming HTTP request
       """
        authorization = request.headers.get("Authorization")
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Invalid or missing token")

        token = authorization.split("Bearer ")[1]
        # Validate the token using the selected handler
        check_token = self.auth_handler.validate_token(token)
        if check_token:
            # If valid, read data from the token and attach to request state
            read_token_data = self.auth_handler.read_data(token)
            request.state.user_id = read_token_data["user_id"]
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
