from typing import Dict, List, Union

from lib_archi.abstractions.non_resource_app_service_interface import ILibNonResourceService
from lib_archi.abstractions.non_resource_controller_interface import ILibNonResourceController
from lib_archi.abstractions.request_interface import IRequest
from lib_archi.utils.enforce_request_interface import enforce_request_type

class NonResourceController(ILibNonResourceController):
    """
    Controller class for handling non-resource-related operations.

    This class acts as an intermediary between the request handler and the application 
    service, delegating logic execution to `NonResourceAppService` and formatting responses 
    using the provided response handler.
    """

    def __init__(self, non_resource_app_service: ILibNonResourceService,):
        """
        Initializes the controller with a service instance and a response handler.

        Args:
            non_resource_app_service (ILibNonResourceService): The application service 
                responsible for executing non-resource logic.
        """
        self.non_resource_app_service: ILibNonResourceService = non_resource_app_service

    @enforce_request_type()
    def perform(self, request: IRequest) -> Dict[str, Union[str, int, Dict, List]]:
        """
        Processes the request and returns a formatted response.

        Args:
            request: The request object containing the necessary data.

        Returns:
            Dict[str, Union[str, int, Dict, List]]: A structured response dictionary.

        Notes:
            - Delegates the request to `non_resource_app_service.perform()`.
            - If successful, formats the response with a success message.
            - If an exception occurs, returns an error response with status code 400.
        """
        return self.non_resource_app_service.perform(request)
    
    def websocket_setup(self, websocket):
        return self.non_resource_app_service.websocket_setup(websocket)

    def websocket_msg_receiver(self, websocket, msg: str):
       return self.non_resource_app_service.websocket_msg_receiver(websocket, msg)
