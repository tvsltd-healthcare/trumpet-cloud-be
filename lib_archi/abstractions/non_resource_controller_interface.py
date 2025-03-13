from abc import ABC, abstractmethod
from typing import Optional

from lib_archi.abstractions.non_resource_app_service_interface import ILibNonResourceService



class ILibNonResourceController(ABC):
    """
    """

    @abstractmethod
    def __init__(self, non_resource_app_service: ILibNonResourceService) -> Optional[object]:
        pass
    
    @abstractmethod
    def perform(self, request: object) -> Optional[object]:
        """
        """
        pass
