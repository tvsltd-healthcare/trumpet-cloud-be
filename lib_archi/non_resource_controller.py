from typing import Dict, List, Union

from adapters.response_adapters.response_handler import ResponseHandler
from lib_archi.abstractions.non_resource_app_service_interface import ILibNonResourceService
from lib_archi.abstractions.non_resource_controller_interface import ILibNonResourceController

class NonResourceController(ILibNonResourceController):
    """
    Controller class for handling non-resource-related operations.

    This class acts as an intermediary between the request handler and the application 
    service, delegating logic execution to `NonResourceAppService` and formatting responses 
    using the provided response handler.
    """

    def __init__(self, non_resource_app_service: ILibNonResourceService, response_handler: ResponseHandler):
        """
        Initializes the controller with a service instance and a response handler.

        Args:
            non_resource_app_service (ILibNonResourceService): The application service 
                responsible for executing non-resource logic.
            response_handler: A handler used for formatting success and error responses.
        """
        self.non_resource_app_service: ILibNonResourceService = non_resource_app_service
        self.response_handler = response_handler

    def perform(self, request) -> Dict[str, Union[str, int, Dict, List]]:
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
        try:
            service_response = self.non_resource_app_service.perform(request)
            return self.response_handler.resource_detail(
                "Operation successful", data=service_response, status_code=200
            )
        except Exception as e:
            return self.response_handler.error_response(f"{str(e)}", 400)
