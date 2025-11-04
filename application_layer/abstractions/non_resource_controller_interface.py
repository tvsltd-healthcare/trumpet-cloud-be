from abc import ABC, abstractmethod
from typing import Dict, List, Union

class INonResourceController(ABC):
    """
    Abstract base class for non-resource controllers.
    
    This interface defines a contract for handling non-resource-related requests 
    in a structured manner. Implementing classes should provide a concrete 
    implementation of the `perform` method to process incoming requests.
    """
    
    @abstractmethod
    def perform(self, request) -> Dict[str, Union[str, int, Dict, List]]:
        """
        Processes a request and returns a structured response.
        
        Args:
            request: The request object containing necessary parameters.
        
        Returns:
            Dict[str, Union[str, int, Dict, List]]: A dictionary containing 
            the response data. The response may include:
                - Strings (e.g., status messages)
                - Integers (e.g., status codes)
                - Nested dictionaries (e.g., detailed response data)
                - Lists of dictionaries (e.g., collections of related information)
        
        Implementing classes should define the exact response structure based 
        on the specific use case.
        """
        pass
