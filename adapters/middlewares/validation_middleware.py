from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from adapters.entity_adapters.entity_validation import EntityAdapter
from application_layer.entities import get_resource_types

from adapters.utils.utils import load_config, get_model_name

entity_resources = get_resource_types()


class ValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for validating incoming requests.

    This middleware intercepts POST, PUT, and PATCH requests before they reach the request handler
    and validates the request body based on the configured models in the config file.
    """
    def __init__(self, app):
        super().__init__(app)
        # Load the configuration file
        self.configs = load_config()

    async def dispatch(self, request: Request, call_next):
        """Process incoming requests and validate them if necessary.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next function in the middleware chain.

        Returns:
            Response: A JSONResponse if validation fails, or the next middleware response if validation passes.
        """
        configs = self.configs

        # todo: when we will get File from request.file - we will get the associated fields from request.form
        # for now quick fix on not to check when file is uploaded via form data
        content_type = request.headers.get("content-type", "")
        if request.method in {'POST', 'PUT', 'PATCH'} and "application/json" in content_type:
            try:
                body = await request.json()
            except Exception:
                return JSONResponse(content={"message": "Invalid JSON format", }, status_code=422)

            model_name = get_model_name(request.url.path, request.method, configs)

            if model_name and model_name in entity_resources:
                validation_result = EntityAdapter().validate(entity_name=entity_resources[model_name], data=body)
                if validation_result is not True:
                    return JSONResponse(content=validation_result, status_code=422)

        # Continue with request processing if validation passes
        return await call_next(request)


