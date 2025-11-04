from typing import Protocol, List, Dict

from domain_layer.abstractions.websocket_wrapper_interface import IWebSocketWrapper


class IWebsocketPool(Protocol):
    def register(self, resource_id: str, websocket: IWebSocketWrapper) -> None:
        ...

    def disconnect(self, resource_id: str, websocket: IWebSocketWrapper) -> None:
        ...

    def broadcast(self, resource_id: str, message: str) -> None:
        ...

    def broadcast_json(self, resource_id: str, data: dict) -> None:
        ...
