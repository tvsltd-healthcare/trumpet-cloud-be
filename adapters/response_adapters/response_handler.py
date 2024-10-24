import json
from typing import Dict, List, Any

from application_layer.abstractions.response_interface import IResponseHandler


class ResponseHandler(IResponseHandler):
    """
    A handler that implements the IResponseHandler interface for generating
    standardized HTTP responses in a structured JSON format.
    """

    def resource_list(self, message: str, data: List[Any] = None, status_code: int = 200) -> str:
        """
        Generates a JSON response for retrieving multiple resource items.
        """
        response = {
            "message": message,
            "data": data or [],
            "status_code": status_code
        }
        return json.dumps(response)

    def resource_detail(self, message: str, data: Dict[str, Any] = None, status_code: int = 200) -> str:
        """
        Generates a JSON response for retrieving a single resource item.
        """
        response = {
            "message": message,
            "data": data or {},
            "status_code": status_code
        }
        return json.dumps(response)

    def resource_created(self, message: str, data: Dict[str, Any], status_code: int = 201) -> str:
        """
        Generates a JSON response for successfully creating a resource item.
        """
        response = {
            "message": message,
            "data": data,
            "status_code": status_code
        }
        return json.dumps(response)

    def error_response(self, message: str, status_code: int = 401) -> str:
        """
        Generates a JSON response for general error issues.
        """
        response = {
            "message": message,
            "status_code": status_code
        }
        return json.dumps(response)

    def validation_error(self, message: str, errors: List[Dict[str, str]], status_code: int = 422) -> str:
        """
        Generates a JSON response for validation errors.
        """
        response = {
            "message": message,
            "errors": errors,
            "status_code": status_code
        }
        return json.dumps(response)

