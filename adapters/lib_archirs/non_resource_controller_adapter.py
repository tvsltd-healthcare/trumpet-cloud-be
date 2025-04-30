from typing import Dict, List, Union
from application_layer.abstractions.non_resource_controller_interface import INonResourceController
from application_layer.abstractions.response_interface import IResponseHandler
from lib_archi.abstractions.non_resource_controller_interface import ILibNonResourceController

from fastapi import Request


class NonResourceControllerAdapter(INonResourceController):
    """
    Adapter class that wraps an instance of INonResourceController.
    This adapter allows for potential modifications or extensions of the controller behavior
    while maintaining the same interface.
    """

    def __init__(self, non_resource_controller: ILibNonResourceController, response_handler: IResponseHandler):
        self.non_resource_controller = non_resource_controller
        self.response_handler = response_handler

    def perform(self, request: Request) -> Dict[str, Union[str, int, Dict, List]]:
        """
        Calls the `perform` method of the wrapped `non_resource_controller` instance.

        :param request: The FastAPI request object containing request data.
        :return: The response from the underlying controller's `perform` method.
        """
        try:
            service_response = self.non_resource_controller.perform(request)

            return self.response_handler.generate_response(
                message=service_response.get('message', ''), data=service_response.get('data', {}),
                status_code=service_response.get('status_code', '')
            )
        except Exception as e:
            return self.response_handler.generate_response(f"{str(e)}", 400)
