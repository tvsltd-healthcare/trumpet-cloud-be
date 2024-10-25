from typing import Dict, List, Any
from application_layer.abstractions.response_interface import IResponseHandler


class ResponseHandler(IResponseHandler):
    """
    A handler that implements the IResponseHandler interface for generating
    standardized HTTP responses in a structured JSON format.
    """

    def resource_list(self, message: str, data: Dict[str, Any] = None, status_code: int = 200) -> Dict[str, Any]:
        """
        Generates a JSON response for retrieving multiple resource items.
        """
        return {
            "message": message,
            "data": data or [],
            "status_code": status_code
        }

    def resource_detail(self, message: str, data: Dict[str, Any] = None, status_code: int = 200) -> Dict[str, Any]:
        """
        Generates a JSON response for retrieving a single resource item.
        """
        return {
            "message": message,
            "data": data or {},
            "status_code": status_code
        }

    def error_response(self, message: str, status_code: int = 401) -> Dict[str, Any]:
        """
        Generates a JSON response for general error issues.
        """
        return {
            "message": message,
            "status_code": status_code
        }

    def validation_error(self, message: str, errors: List[Dict[str, str]], status_code: int = 422) -> Dict[str, Any]:
        """
        Generates a JSON response for validation errors.
        """
        return {
            "message": message,
            "errors": errors,
            "status_code": status_code
        }
