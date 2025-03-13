from abc import ABC, abstractmethod
from typing import Dict, Optional


class INonResourceAppService(ABC):
    """
    """

    @abstractmethod
    def __init__(self, logic_map: Dict[str, object]) -> Optional[object]:
        pass

    @abstractmethod
    def _get_logic(self, request) -> Optional[object]:
        """
        """
        pass
    
    @abstractmethod
    def perform(self, request) -> Optional[object]:
        """
        """
        pass

    
