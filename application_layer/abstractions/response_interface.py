from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional


class IResponseHandler(ABC):
    """
    Interface for a response handler to generate structured JSON API responses.
    """

    @abstractmethod
    def generate_response(self, message: str, status_code: int = 200, data: Optional[Any] = None,
                          errors: Optional[List[Dict[str, str]]] = None, ) -> Dict[str, Any]:
        pass
