from typing import Dict, List, Any, Optional
from application_layer.abstractions.response_interface import IResponseHandler


class ResponseHandler(IResponseHandler):
    """
    A handler that implements the IResponseHandler interface for generating
    standardized HTTP responses in a structured JSON format.
    """

    def generate_response(
            self,
            message: str,
            status_code: int = 200,
            data: Optional[Any] = None,
            errors: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Generates a standardized JSON response for various use cases,
        including success, error, and validation responses.

        :param message: The response message.
        :param status_code: The HTTP status code (default: 200).
        :param data: The response data, which can be a dictionary or list (default: None).
        :param errors: A list of validation errors (default: None).
        :return: A structured JSON response.
        """
        response = {
            "message": message,
            "status_code": status_code
        }
        if isinstance(data, (dict, list)) and data:
            response["data"] = data

        if errors is not None:
            response["errors"] = errors

        return response
