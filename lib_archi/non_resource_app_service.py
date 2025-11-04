from typing import Optional, Dict

from lib_archi.abstractions.non_resource_app_service_interface import ILibNonResourceService
from lib_archi.abstractions.request_interface import IRequest


class NonResourceAppService(ILibNonResourceService):
    """
    Service class for handling non-resource-related application logic.

    This class provides a mechanism to route requests to the appropriate logic 
    based on the request path. It looks up logic handlers from a predefined 
    `logic_map` and invokes them dynamically.
    """

    def __init__(self, logic_map: Dict):
        """
        Initializes the service with a logic map.

        Args:
            logic_map (Dict): A dictionary mapping request paths to logic handlers.
        """
        self.logic_map: Dict = logic_map

    def _get_logic(self, request: IRequest) -> Optional[object]:
        """
        Retrieves the corresponding logic handler for the given request.

        Args:
            request: The request object containing the URL path.

        Returns:
            Optional[object]: The logic handler if found, otherwise None.
        
        Notes:
            - Extracts the path after "api/" and replaces "/" with "_".
            - Uses the modified path to look up the logic in `logic_map`.
        """
        path: str = request.get_path().split("api/")[-1]

        if path:
            path = path.replace("/", "_")
            path = path.replace("-", "_")

        return self.logic_map.get(path, None)

    def perform(self, request: IRequest) -> Optional[object]:
        """
        Executes the logic associated with the request path.

        Args:
            request: The request object containing relevant data.

        Returns:
            Optional[object]: The result of executing the logic handler.

        Raises:
            NotImplementedError: If no logic is defined for the requested path.

        Notes:
            - Uses `_get_logic` to retrieve the appropriate logic handler.
            - If a handler is found, it is executed with the request object.
            - If no handler is found, a `NotImplementedError` is raised.
        """
        logic = self._get_logic(request)

        if logic:
            return logic(request)
        else:
            raise NotImplementedError("Logic for this endpoint is not implemented")

    def websocket_setup(self, websocket):
        logic = self._get_logic(websocket)

        if logic:
            return logic(websocket)
        else:
            raise NotImplementedError("Logic for this endpoint is not implemented")

    def websocket_msg_receiver(self, websocket, msg: str, event: str):
        logic = self.logic_map.get('websocket_msg_receiver', None)

        if logic:
            return logic(websocket, msg, event)
        else:
            raise NotImplementedError("Logic for this endpoint is not implemented")
