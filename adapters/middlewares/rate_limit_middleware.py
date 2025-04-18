import time
from collections import defaultdict
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, rate_limit: int, time_window: int):
        super().__init__(app)
        self.rate_limit = rate_limit  # Max requests allowed
        self.time_window = time_window  # Time window in seconds
        self.request_counts = defaultdict(list)  # Store request timestamps per IP

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        if forwarded := request.headers.get("X-Forwarded-For"):
            client_ip = forwarded.split(",")[0].strip()

        current_time = time.time()

        # Remove old timestamps outside the time window
        self.request_counts[client_ip] = [
            timestamp for timestamp in self.request_counts[client_ip]
            if timestamp > current_time - self.time_window
        ]

        # Check if the rate limit is exceeded
        if len(self.request_counts[client_ip]) >= self.rate_limit:
            return JSONResponse(
                status_code=429,
                content={"message": "Too many requests. Try again later."}
            )

        # Log the request timestamp
        self.request_counts[client_ip].append(current_time)

        return await call_next(request)


def rate_limit_middleware_factory(rate_limit: int, time_window: int):
    """
    Factory function to create a RateLimitMiddleware with specified parameters.

    Args:
        rate_limit: Maximum number of requests allowed within the time window
        time_window: Time window in seconds

    Returns:
        A function that takes an app instance and returns a configured middleware
    """

    def create_middleware(app: FastAPI):
        return RateLimitMiddleware(app, rate_limit=rate_limit, time_window=time_window)

    return create_middleware
