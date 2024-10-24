from abc import ABC, abstractmethod
from typing import Any, List, Dict


class IResponseHandler(ABC):
    """
    Interface for a response handler to generate structured JSON API responses.
    """

    @abstractmethod
    def resource_list(self, message: str, data: List[Any] = None, status_code: int = 200) -> str:
        pass

    @abstractmethod
    def resource_detail(self, message: str, data: Dict[str, Any] = None, status_code: int = 200) -> str:
        pass

    @abstractmethod
    def resource_created(self, message: str, data: Dict[str, Any], status_code: int = 201) -> str:
        pass

    @abstractmethod
    def error_response(self, message: str, status_code: int = 401) -> str:
        pass

    @abstractmethod
    def validation_error(self, message: str, errors: List[Dict[str, str]], status_code: int = 422) -> str:
        pass
