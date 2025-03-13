from abc import ABC, abstractmethod
from typing import Optional

from application_layer.abstractions.non_resource_app_service_interface import INonResourceAppService


class INonResourceController(ABC):
    """Abstract base class for handling CRUD operations on entities.

    This interface defines the structure for classes responsible for creating,
    retrieving, updating, and deleting entities, as well as handling collections of entities.
    Implementing classes must define methods for each CRUD operation.
    """

    @abstractmethod
    def __init__(self, non_resource_app_service: INonResourceAppService) -> Optional[object]:
        pass
    
    @abstractmethod
    def perform(self, request) -> Optional[object]:
        """Abstract method for creating a new entity.

         Args:
             entity (object): The entity object containing data for creation.
             request (object): Additional request context or parameters.

         Returns:
             Optional[object]: The created entity object, or None if creation fails.

         Raises:
             NotImplementedError: This method must be implemented in subclasses.
         """
        pass

    
