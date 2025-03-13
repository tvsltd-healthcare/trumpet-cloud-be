from typing import Dict, Optional

from application_layer.abstractions.non_resource_app_service_interface import INonResourceAppService


class NonResourceAppServiceAdapter(INonResourceAppService):
    """
    """

    def __init__(self, non_resource_app_service:INonResourceAppService):
        """
        """
        self.non_resource_app_service: INonResourceAppService = non_resource_app_service

    def _get_logic(self, request) -> Optional[object]:
        """
        """
        path: str = request.url.path.split("api/")[-1]
        logic_map = self.non_resource_app_service.logic_map
        return logic_map.get(path, None)

    def perform(self, request):
        """
        """
        print("got into app service adapter with this request", request)

        logic = self._get_logic(request)
        return self.non_resource_app_service.perform(request, logic)
