import uuid
from datetime import datetime

from typing import Optional, Dict

from application_layer.abstractions.non_resource_app_service_interface import INonResourceAppService
from application_layer.abstractions.non_resource_controller_interface import INonResourceController
from lib_archi.abstractions.non_resource_controller_interface import ILibNonResourceController
from .base_application_service import BaseApplicationService
from application_layer.abstractions.response_interface import IResponseHandler




class NonResourceController(ILibNonResourceController):
    """A generic base controller for handling CRUD operations on entities.

    This class defines the standard CRUD (Create, Read, Update, Delete) methods
    for an entity by utilizing the corresponding application service.

    Attributes:
        app_service (BaseApplicationService[Entity]): The application service that
            performs operations on the entity.

    Args:
        app_service (BaseApplicationService[Entity]): The service for handling
            the business logic related to the entity.
    """

    def __init__(self, non_resource_app_service: INonResourceAppService, response_handler: IResponseHandler):
        """
        """
        
        self.non_resource_app_service: INonResourceAppService = non_resource_app_service
        self.response_handler: IResponseHandler = response_handler

    def perform(self, request) -> Optional[object]:
        """
        """
        try:
            service_response = self.non_resource_app_service.perform(request)
            return self.response_handler.resource_detail("Operation successful", data=service_response, status_code=200)
        except Exception as e:
            return self.response_handler.error_response(f"{str(e)}", 400)
    