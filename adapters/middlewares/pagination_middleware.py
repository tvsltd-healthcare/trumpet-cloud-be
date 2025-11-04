import re

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from typing import Callable
import json
from urllib.parse import urlencode


class PaginationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, per_page: int):
        super().__init__(app)
        self.per_page = per_page

    """
    Middleware for paginating JSON API responses.
    Args:
        app: FastAPI application instance
        per_page: Number of items per page
            
    """
    async def dispatch(self, request: Request, call_next: Callable):
        # Get page and per_page from query params
        page = int(request.query_params.get("page", 1))
        per_page = int(request.query_params.get("per_page", self.per_page))
        offset = (page - 1) * per_page

        # Make the request and get response
        response = await call_next(request)
        pattern = r"^/api/[^/]+/?$"

        # Check if method is GET and matches the pattern
        if request.method == "GET" and re.match(pattern, request.url.path):
            # Ensure we only apply pagination on JSON responses
            if "application/json" in response.headers.get("content-type", ""):
                response_body = [section async for section in response.body_iterator]
                raw_data = b"".join(response_body)
                parsed = json.loads(raw_data)

                # Extract actual data list
                data_list = parsed.get("data")
                if isinstance(data_list, list):
                    total = len(data_list)
                    paginated_data = data_list[offset: offset + per_page]

                    last_page = (total + per_page - 1) // per_page  # Ceiling division
                    path = str(request.base_url)[:-1] + str(request.url.path)
                    base_query = dict(request.query_params)
                    base_query.pop("page", None)

                    def build_url(p):
                        return f"{path}?{urlencode({**base_query, 'page': p})}"

                    # Generate pagination links
                    links = []

                    if page > 1:
                        links.append({
                            "url": build_url(page - 1),
                            "label": "Previous",
                            "active": False
                        })

                    for i in range(1, last_page + 1):
                        links.append({
                            "url": build_url(i),
                            "label": str(i),
                            "active": i == page
                        })

                    if page < last_page:
                        links.append({
                            "url": build_url(page + 1),
                            "label": "Next",
                            "active": False
                        })

                    formatted = {
                        "current_page": page,
                        "first_page_url": build_url(1),
                        "last_page": last_page,
                        "last_page_url": build_url(last_page),
                        "next_page_url": build_url(page + 1) if page < last_page else None,
                        "path": path,
                        "per_page": per_page,
                        "prev_page_url": build_url(page - 1) if page > 1 else None,
                        "total": total
                    }

                    new_response = {
                        "message": parsed.get("message"),
                        "status_code": response.status_code,
                        "data": paginated_data,
                        "meta": formatted,
                        "links": links
                    }
                    return JSONResponse(content=new_response, status_code=response.status_code)

        return response


def pagination_middleware(per_page: int):
    """
    Factory function to create a PaginationMiddleware with specified parameters.

    Args:
        per_page: Number of items per page

    Returns:
        A function that takes an app instance and returns a configured middleware
    """

    def create_middleware(app: FastAPI):
        return PaginationMiddleware(app, per_page=per_page)

    return create_middleware
