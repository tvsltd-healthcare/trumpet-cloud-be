from domain_layer.abstractions.websocket_pool_interface import IWebsocketPool
from domain_layer.abstractions.websocket_wrapper_interface import IWebSocketWrapper


class WebsocketPoolAdapter(IWebsocketPool):
    def __init__(self, manager: IWebsocketPool):
        self._manager = manager

    def register(self, resource_id: str, websocket: IWebSocketWrapper) -> None:
        self._manager.register(resource_id, websocket)
    
    def disconnect(self, resource_id: str, websocket: IWebSocketWrapper) -> None:
        self._manager.disconnect(resource_id, websocket)

    def broadcast(self, resource_id: str, message: str) -> None:
        self._manager.broadcast(resource_id, message)

    def broadcast_json(self, resource_id: str, data: dict) -> None:
        self._manager.broadcast_json(resource_id, data)
