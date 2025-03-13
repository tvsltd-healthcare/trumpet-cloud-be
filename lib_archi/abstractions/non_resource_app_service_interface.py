from abc import ABC, abstractmethod
from typing import Optional


class ILibNonResourceService(ABC):
    """
    """

    @abstractmethod
    def perform(self, request: object) -> Optional[object]:
        """
        """
        pass
