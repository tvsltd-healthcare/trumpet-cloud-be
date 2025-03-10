import json
from typing import Callable, List

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response, StreamingResponse


class ResponseMiddleware(BaseHTTPMiddleware):
    """
    Middleware for standardizing HTTP responses with route exclusions.
    """

    def __init__(self, app, exclude_routes: List[str] = None):
        super().__init__(app)
        # Default routes to exclude, including all Swagger/OpenAPI related routes
        default_excludes = [
            "/health",
            "/status",
            "/docs",
            "/docs/oauth2-redirect",
            "/redoc",
            "/openapi.json",
            "/swagger-ui.css",
            "/swagger-ui-bundle.js",
            "/swagger-ui-standalone-preset.js",
            "/favicon.ico"
        ]
        # Combine default excludes with any additional routes
        self.exclude_routes = default_excludes + (exclude_routes or [])
        # Ensure all routes are properly formatted
        self.exclude_routes = [route.rstrip('/') for route in self.exclude_routes]

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and standardize the response format.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next function in the middleware chain.

        Returns:
            Response: A standardized JSONResponse or the original response for excluded routes.
        """
        # Normalize the request path by removing trailing slash
        current_path = request.url.path.rstrip('/')

        # Check if the current path matches any excluded route exactly
        # or if it starts with /docs/ (for dynamic swagger routes)
        if current_path in self.exclude_routes or current_path.startswith('/docs/'):
            return await call_next(request)

        # Process the request
        response = await call_next(request)

        # Handle JSON responses
        if isinstance(response, Response):
            try:
                # Read the body content, handling StreamingResponse differently
                if isinstance(response, StreamingResponse):
                    content = b"".join([chunk async for chunk in response.body_iterator])
                else:
                    content = await response.body()

                # Try to decode and parse JSON content
                try:
                    data = json.loads(content.decode())
                except UnicodeDecodeError:
                    # If content can't be decoded as UTF-8, return original response
                    return response

                # Standardize the response format
                standardized_response = {
                    "message": data.get("message", "Request processed successfully"),
                    "status_code": data.get("status_code", response.status_code)
                }

                # Include optional fields if they exist
                for key in ("data", "errors", "detail"):
                    if key in data:
                        standardized_response["message" if key == "detail" else key] = data[key]

                return JSONResponse(
                    content=standardized_response,
                    status_code=standardized_response["status_code"]
                )

            except json.JSONDecodeError:
                # If the response isn't JSON, return it as is
                return response

        return response
