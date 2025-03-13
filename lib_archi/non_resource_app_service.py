import uuid
from datetime import datetime

from typing import Optional, Dict

from application_layer.abstractions.non_resource_app_service_interface import INonResourceAppService
from application_layer.abstractions.non_resource_controller_interface import INonResourceController
from lib_archi.abstractions.non_resource_app_service_interface import ILibNonResourceService
from .base_application_service import BaseApplicationService
from application_layer.abstractions.response_interface import IResponseHandler




class NonResourceAppService(ILibNonResourceService):
    """
    """

    def __init__(self,  logic_map: Dict):
        """
        """
        self.logic_map: Dict = logic_map

    def perform(self, request, logic) -> Optional[object]:
        # todo: need to check if we could do downcastnig request to our IRequest here by type
        """
        """
        if logic:
            return logic(request)
        else:
            raise NotImplementedError("Logic for this endpoint is not implemented")
    