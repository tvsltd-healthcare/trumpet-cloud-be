import os
import re
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

def normalize_host(host: str) -> str:
    """
    Normalize host by removing http(s) protocol and lowercasing.
    """
    return re.sub(r"^https?://", "", host.strip().lower())

def get_client_ip(request: Request) -> str:
    try:
        # Check common proxy headers in order of trust
        x_forwarded_for = request.headers.get("x-forwarded-for")
        if x_forwarded_for:
            # May contain multiple IPs, client IP is usually the first
            return x_forwarded_for.split(",")[0].strip()

        x_real_ip = request.headers.get("x-real-ip")
        if x_real_ip:
            return x_real_ip.strip()

        # Fall back to raw socket client IP
        return request.client.host
    except Exception as e:
        print(f"Error getting client IP: {e}")
        return ""

class AllowedHostMiddleware(BaseHTTPMiddleware):
    """
    Middleware for validating the Host header against allowed hosts (including ports).

    Ensures that requests only come from trusted domains and ports defined in ALLOWED_HOSTS and also not from black listed ips.
    """

    def __init__(self, app):
        super().__init__(app)
        raw_hosts = os.getenv("ALLOWED_HOSTS", "")
        raw_blacklisted_ips = os.getenv("BLACKLISTED_IPS", "")
        self.allowed_hosts = {normalize_host(h) for h in raw_hosts.split(",") if h.strip()}
        self.blacklisted_ips = {h.strip() for h in raw_blacklisted_ips.split(",") if h.strip()}

    async def dispatch(self, request: Request, call_next):
        """
        Block request if host:port is not in the allowed list.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next middleware or route handler.

        Returns:
            JSONResponse or next response in chain.
        """
        host_header = normalize_host(request.headers.get("host", ""))
        client_ip = get_client_ip(request)

        print('client_ip', client_ip)

        is_host_invalid = (
            "*" not in self.allowed_hosts and host_header not in self.allowed_hosts
        )

        print('self.blacklisted_ips', self.blacklisted_ips)

        is_ip_blacklisted = (
            "*" in self.blacklisted_ips or client_ip in self.blacklisted_ips
        )

        if is_host_invalid or is_ip_blacklisted:
            print(f"Forbidden - Host:'{host_header}' IP:'{client_ip}' is not allowed")

            return JSONResponse(
                content={"message": "Bad Request", "status_code": 400},
                status_code=400
            )

        return await call_next(request)
