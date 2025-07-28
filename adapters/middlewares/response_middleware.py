import json
from typing import Callable, List, Dict, Optional, Any, Union

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response, StreamingResponse
from adapters.utils.utils import load_config, get_model_name


class ResponseMiddleware(BaseHTTPMiddleware):
    """
    Middleware for standardizing HTTP responses with route exclusions.
    """

    def __init__(self, app, exclude_routes: List[str] = None):
        super().__init__(app)
        # Default routes to exclude, including all Swagger/OpenAPI related routes
        default_excludes = ["/health", "/status", "/docs", "/docs/oauth2-redirect", "/redoc", "/openapi.json",
            "/swagger-ui.css", "/swagger-ui-bundle.js", "/swagger-ui-standalone-preset.js", "/favicon.ico"]
        # Combine default excludes with any additional routes
        self.exclude_routes = default_excludes + (exclude_routes or [])
        # Ensure all routes are properly formatted
        self.exclude_routes = [route.rstrip('/') for route in self.exclude_routes]
        self.configs = load_config()

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

        if response.headers.get('content-type') != 'application/json':
            return response

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
                    print(data)
                    # check if data json has key named data exists
                    if "data" in data:
                        # If data is not None, use it as the response body
                        self.format_response(data, request)
                except UnicodeDecodeError as e:
                    # If content can't be decoded as UTF-8, return original response
                    return response
                except Exception as e:
                    print("Exception", e)

                # Standardize the response format
                standardized_response = {"message": data.get("message", "Request processed successfully"),
                    "status_code": data.get("status_code", response.status_code)}

                # Include optional fields if they exist
                for key in ("data", "errors", "detail"):
                    if key in data:
                        standardized_response["message" if key == "detail" else key] = data[key]

                return JSONResponse(content=standardized_response, status_code=standardized_response["status_code"])

            except json.JSONDecodeError:
                # If the response isn't JSON, return it as is
                return response
        else:
            return response

    def format_response(self, response_body, request: Request) -> dict:
        """
        Format the response body based on the model name and configuration.
        Args:
            response_body: Response body to be formatted.
            request: Request object containing the HTTP request information.
        Returns:
            dict: Formatted response body.
        """
        configs = self.configs
        model_name = get_model_name(request.url.path, request.method, configs)
        if not model_name:
            return response_body
        else:
            response_body_data = response_body["data"]
            if response_body_data.get('ignore_response') is True:
                response_body_data.pop("ignore_response", None)
                return response_body
            # Get the attributes of the model based on the model name
            get_model_attributes = self.get_model_attributes(model_name, configs[0]['models'])
            if not get_model_attributes:
                return response_body
            # Check if the model name is in the response body
            filtered_json = self.filter_input_by_schema(get_model_attributes, response_body["data"])
            response_body["data"] = filtered_json
            return response_body

    def filter_input_by_schema(self, schema: List[Dict[str, Any]],
                               input_data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Union[
        Dict[str, Any], List[Dict[str, Any]]]:

        """
        Filter the input data based on the schema provided.
        Args:
            schema: Configuration schema defining the allowed fields.
            input_data: Input data to be filtered, can be a dictionary or a list of dictionaries.
        Returns:
            Union[Dict[str, Any], List[Dict[str, Any]]]: Filtered input data.
        """

        # Extract allowed keys based on `in_response` being True or none
        allowed_keys = {field['column'] for field in schema if field.get('in_response') is True or field.get('in_response') is None}

        def filter_dict(data: Dict[str, Any]) -> Dict[str, Any]:
            return {key: value for key, value in data.items() if key in allowed_keys}

        # Handle list of dicts or single dict
        if isinstance(input_data, list):
            return [filter_dict(item) for item in input_data]
        elif isinstance(input_data, dict):
            return filter_dict(input_data)
        else:
            raise TypeError("input_data must be a dictionary or a list of dictionaries")

    def get_model_attributes(self, model_name, models):
        """
        Retrieve the attributes of a model based on its name.
        :param model_name: The name of the model to retrieve attributes for.
        :param models: A list of model definitions.
        :return: A list of attributes for the specified model or None if not found.
        """
        for model in models:
            if model.get("name") == model_name:
                return model.get("attributes", [])
        return None
