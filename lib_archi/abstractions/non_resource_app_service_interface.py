from abc import ABC, abstractmethod
from typing import Optional


class ILibNonResourceService(ABC):
    """
    Abstract interface for a non-resource service.

    This interface defines a contract for handling non-resource-related logic 
    within the application. Implementing classes should provide the actual 
    logic execution by implementing the `perform` method.
    """

    @abstractmethod
    def perform(self, request: object) -> Optional[object]:
        """
        Executes the service logic based on the given request.

        Args:
            request (object): The request object containing relevant data 
                for processing.

        Returns:
            Optional[object]: The result of the execution, which could be 
                any object or `None` if no response is required.

        Notes:
            - This method must be implemented by any subclass.
            - The implementation should handle any necessary business logic 
              and return the appropriate response.
        """
        pass
