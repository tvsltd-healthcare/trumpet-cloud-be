from application_layer.abstractions.non_resource_app_service_interface import INonResourceAppService
from application_layer.abstractions.non_resource_controller_interface import INonResourceController

from fastapi import Request


class NonResourceControllerAdapter(INonResourceController):
    """
    """

    def __init__(self, non_resource_controller):
        """
        """
        self.non_resource_controller = non_resource_controller

    def perform(self, request: Request):
        """
        """
        print("got into controler adapter with this request", request)
        return self.non_resource_controller.perform(request)
    