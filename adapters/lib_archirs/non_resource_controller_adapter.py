from typing import Dict, List, Union

from fastapi import Request
from starlette.responses import FileResponse

from application_layer.abstractions.non_resource_controller_interface import INonResourceController
from application_layer.abstractions.response_interface import IResponseHandler
from lib_archi.abstractions.non_resource_controller_interface import ILibNonResourceController


class NonResourceControllerAdapter(INonResourceController):
    """
    Adapter class that wraps an instance of INonResourceController.
    This adapter allows for potential modifications or extensions of the controller behavior
    while maintaining the same interface.
    """

    def __init__(self, non_resource_controller: ILibNonResourceController, response_handler: IResponseHandler):
        self.non_resource_controller = non_resource_controller
        self.response_handler = response_handler

    def perform(self, request: Request) -> Union[Dict[str, Union[str, int, Dict, List]], FileResponse]:
        """
        Calls the `perform` method of the wrapped `non_resource_controller` instance.

        :param request: The FastAPI request object containing request data.
        :return: The response from the underlying controller's `perform` method.
        """
        try:
            service_response = self.non_resource_controller.perform(request)

            if isinstance(service_response, FileResponse):
                return service_response

            return self.response_handler.generate_response(
                message=service_response.get('message', ''), data=service_response.get('data', {}),
                status_code=service_response.get('status_code', '')
            )
        except Exception as e:
            return self.response_handler.generate_response(f"{str(e)}", 400)
        
    def websocket_setup(self, websocket):
        self.non_resource_controller.websocket_setup(websocket)
        
    def websocket_msg_receiver(self, websocket, msg: str):
        self.non_resource_controller.websocket_msg_receiver(websocket, msg)
