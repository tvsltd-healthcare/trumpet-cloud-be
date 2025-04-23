"""FastAPI authorization middleware for request-level permission checks.

This module implements a middleware that performs authorization checks for incoming
HTTP requests using a configured authorizer. It extracts user, resource, and
action information from requests to determine if access should be granted.

The middleware supports:
- User identification from request state
- Resource type and ID extraction from URLs
- HTTP method to permission mapping
- Parent resource resolution for hierarchical structures

Classes:
    AuthorizationMiddleware: Main middleware class for authorization checks.

Example:
    >>> app = FastAPI()
    >>> auth_middleware = AuthorizationMiddleware(authorizer=my_authorizer)
    >>> app.middleware("http")(auth_middleware)
"""

import re

from fastapi import Request, HTTPException
from starlette import status

from adapters.middlewares.validation_middleware import ValidationMiddleware


class AuthorizationMiddleware:
    """FastAPI middleware for handling request authorization.

    Performs authorization checks by combining user identity, resource information,
    and requested action to determine if access should be granted.
    """

    def __init__(self, authorizer):
        """Initialize the authorization middleware.

        Args:
            authorizer: Authorization service instance that implements the check method
                for verifying permissions.
        """
        self.authorizer = authorizer
        self.configs = ValidationMiddleware._load_config()

    def __call__(self, request: Request):
        """Process the incoming request and perform authorization check.

        Args:
            request: FastAPI Request object containing request details.

        Raises:
            HTTPException: 403 Forbidden if the authorization check fails.
        """
        user_id = request.state.user_id
        relation = _get_relation(request=request)
        resource = _get_resource(request, configs=self.configs)

        authorization_response = self.authorizer.check(
            {
                "user_type": "user",
                "user_id": user_id,
                "resource_type": resource.get("type"),
                "resource_id": resource.get("id"),
                "action": relation
            }
        )

        if not authorization_response.get("allowed"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def _get_user(request):
    """Extract user information from request headers.

    Args:
        request: FastAPI Request object.

    Returns:
        set: Set containing the user ID extracted from headers.
    """
    user_id = request.headers["userid"]
    return {user_id}


def _get_resource(request, configs):
    """Extract resource information from the request URL and configuration.

    Args:
        request: FastAPI Request object.
        configs: Configuration dictionary containing model definitions.

    Returns:
        dict: Resource information with keys:
            - type: Resource type name
            - id: Resource identifier
    """
    resource_type = ValidationMiddleware._get_model_name(
        request=request, configs=configs
    )
    match = re.search(r"\d+$", str(request.url))
    resource_id = match.group(0)

    if request.method == 'POST':
        _get_parent(resource_type, )
    return {"type": resource_type, "id": resource_id}


def _get_relation(request: Request):
    """Map HTTP method to corresponding permission relation.

    Args:
        request: FastAPI Request object.

    Returns:
        str: HTTP method string representing the permission relation.
    """
    http_method = request.method
    return http_method


def _get_parent(resource_type: str, configs: dict):
    """Determine parent resource type for hierarchical resources.

    Args:
        resource_type: Type of the current resource.
        configs: Configuration dictionary containing model definitions.

    Returns:
        str: Parent resource type or "system" if no associations defined.
    """
    models = configs[0].get("models", []) or []

    model = _find_object(
        objects=models, key="name", value=resource_type
    )

    if not model.get("associations"):
        return "system"

    return model.get()


def _find_object(objects, key, value):
    """Find first object in a list where key matches specified value.

    Args:
        objects: List of dictionaries to search.
        key: Dictionary key to match against.
        value: Value to find.

    Returns:
        dict: Matching object or None if not found.
    """
    return next((obj for obj in objects if obj.get(key) == value), None)
