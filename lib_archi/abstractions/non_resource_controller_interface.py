from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

from lib_archi.abstractions.non_resource_app_service_interface import ILibNonResourceService

class ILibNonResourceController(ABC):
    """
    Abstract interface for a non-resource controller.

    This interface defines a contract for a controller that interacts with 
    a non-resource service (`ILibNonResourceService`). Implementing classes 
    should define the logic for initializing and performing the necessary 
    actions in response to a request, returning structured data.
    """

    @abstractmethod
    def __init__(self, non_resource_app_service: ILibNonResourceService):
        """
        Initializes the controller with the provided application service.

        Args:
            non_resource_app_service (ILibNonResourceService): The service 
                that performs the core logic for non-resource operations.

        Notes:
            - The constructor should establish any necessary connections or 
              dependencies for the controller.
            - This method should be implemented by any subclass.
        """
        pass
    
    @abstractmethod
    def perform(self, request: object) -> Dict[str, Union[str, int, Dict, List]]:
        """
        Processes a request and returns a structured response.

        Args:
            request (object): The request object containing the necessary data 
                to execute the logic.

        Returns:
            Dict[str, Union[str, int, Dict, List]]: A dictionary representing 
            the response, which may include status messages, data, or error codes.

        Notes:
            - This method should be implemented by any subclass.
            - The implementation should handle the business logic and structure 
              the response in a consistent format.
        """
        pass
