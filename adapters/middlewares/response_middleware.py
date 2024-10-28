import json
from typing import Callable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response, StreamingResponse


class ResponseMiddleware(BaseHTTPMiddleware):
    """
    Middleware for standardizing HTTP responses.

    This middleware intercepts all responses and formats them into a consistent
    JSON structure.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and standardize the response format.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next function in the middleware chain.

        Returns:
            Response: A standardized JSONResponse.
        """
        # Process the request
        response = await call_next(request)

        # Check if response is a dict
        if isinstance(response, dict):
            standardized_response = {
                "message": response.get("message", "Request processed successfully"),
                "data": response.get("data", None),
                "status_code": 200  # Assuming success, adjust if needed
            }
            return JSONResponse(content=standardized_response, status_code=200)

        # Handle JSON responses
        if isinstance(response, Response):
            try:
                # Read the body content, handling StreamingResponse differently
                if isinstance(response, StreamingResponse):
                    content = b"".join([chunk async for chunk in response.body_iterator])
                else:
                    content = await response.body()
                # Decode and load content as JSON if possible
                data = json.loads(content.decode())
                standardized_response = {
                    "message": data.get("message", "Request processed successfully"),
                    "status_code": data.get("status_code", 200)
                }
                if data.get("data") is not None:
                    standardized_response["data"] = data["data"]
                status_code = standardized_response["status_code"]
                return JSONResponse(content=standardized_response, status_code=status_code)

            except json.JSONDecodeError:
                # If JSON decoding fails, return a generic error response
                return JSONResponse(
                    content={"message": "Invalid response format"},
                    status_code=500
                )

            # If the response is neither JSON nor dict, return it as is
        return response
