from abc import ABC, abstractmethod
from typing import Any, Dict


class IResponseFormatter(ABC):
    @abstractmethod
    def success(self, data: Any, message: str, status_code: int = 200) -> Dict[str, Any]:
        pass

    @abstractmethod
    def error(self, message: str, status_code: int = 500, data: Any = None) -> Dict[str, Any]:
        pass

    @abstractmethod
    def validation_error(self, errors: Any, message: str, status_code: int = 422) -> Dict[str, Any]:
        pass
