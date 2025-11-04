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

        if isinstance(data, dict):
            inner_data = data.get("data", data)
            _data = inner_data if isinstance(inner_data, (dict, list)) else data
            _status_code = data.get("status_code", status_code)
            _message = data.get("message", message)
        else:
            _data = data
            _status_code = status_code
            _message = message

        response = {
            "message": _message if _message else message,
            "status_code": _status_code if _status_code else status_code,
        }

        if errors is not None:
            response["errors"] = errors

        if data and isinstance(data, list):
            response["data"] = data

        if data and isinstance(data, dict):
            #TODO: Need to test all the nested response issue. Fro resource and non resource API.
            if data.get("status_code") is None or data['status_code'] < 400:
                response["data"] = data if _data is None else _data

            if data.get("errors") is not None:
                response["errors"] = data["errors"]

        return response
