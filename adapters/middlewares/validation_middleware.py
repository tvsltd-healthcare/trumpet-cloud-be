import os
import json

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from adapters.entity_adapters.entity_validation import EntityAdapter
from application_layer.entities import get_resource_types


FILE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_FILE_PATH = os.path.join(FILE_PATH, 'config.json')

entity_resources = get_resource_types()


class ValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for validating incoming requests.

    This middleware intercepts POST, PUT, and PATCH requests before they reach the request handler
    and validates the request body based on the configured models in the config file.
    """

    async def dispatch(self, request: Request, call_next):
        """Process incoming requests and validate them if necessary.

        Args:
            request (Request): The incoming HTTP request.
            call_next (Callable): The next function in the middleware chain.

        Returns:
            Response: A JSONResponse if validation fails, or the next middleware response if validation passes.
        """
        configs = self._load_config()

        if request.method in {'POST', 'PUT', 'PATCH'}:
            try:
                body = await request.json()
            except Exception:
                return JSONResponse(content={"message": "Invalid JSON format", }, status_code=422)

            model_name = self._get_model_name(request, configs)

            if model_name and model_name in entity_resources:
                validation_result = EntityAdapter().validate(entity_name=entity_resources[model_name], data=body)
                if validation_result is not True:
                    return JSONResponse(content=validation_result, status_code=422)

        # Continue with request processing if validation passes
        return await call_next(request)

    @staticmethod
    def _load_config() -> dict:
        """Load the configuration file from disk.

        Returns:
            dict: The parsed configuration data.

        Raises:
            HTTPException: If the config file is not found or contains invalid JSON.
        """
        try:
            with open(CONFIG_FILE_PATH, 'r') as config_file:
                return json.load(config_file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise HTTPException(status_code=500, detail=f"Config file error: {str(e)}")

    @staticmethod
    def _get_model_name(request: Request, configs: dict) -> str | None:
        """Retrieve the model name that matches the request URL and method from the configuration.

        Args:
            request (Request): The incoming HTTP request.
            configs (dict): The loaded configuration file.

        Returns:
            str: The model name if found, otherwise None.
        """
        for model in configs[0].get('models', []):
            for route in model.get('routes', []):
                if route.get('method', '').lower() == request.method.lower() and route.get('url', '').lower() == request.url.path.lower():
                    return model.get('name')
        return None
