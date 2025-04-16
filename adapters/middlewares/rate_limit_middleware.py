import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import time
from collections import defaultdict
load_dotenv()


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, rate_limit: int = int(os.getenv("RATE_LIMIT")), time_window: int = int(os.getenv("TIME_WINDOW"))):
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
