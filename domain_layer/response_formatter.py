from typing import Any, Dict

from domain_layer.abstractions.response_formatter_interface import IResponseFormatter


class ResponseFormatter(IResponseFormatter):
    def success(self, data: Any, message: str, status_code: int = 200) -> Dict[str, Any]:
        return {
            "status_code": status_code,
            "message": message,
            "data": data
        }

    def error(self, message: str, status_code: int = 500, data: Any = None) -> Dict[str, Any]:
        return {
            "status_code": status_code,
            "message": message,
            "error": data
        }

    def validation_error(self, errors: Any, message: str, status_code: int = 422) -> Dict[str, Any]:
        return {
            "status_code": status_code,
            "message": message,
            "validation_errors": errors
        }
