from typing import Protocol, Any, Dict


class IWebSocketWrapper(Protocol):
    def send(self, message: str) -> None:
        ...

    def send_json(self, data: Any) -> None:
        ...

    def close(self) -> None:
        ...

    def get_headers(self) -> Dict[str, Any]:
        ...

    def get_query_params(self) -> Dict[str, Any]:
        ...

    def get_path(self) -> str:
        ...

    def get_path_params(self) -> Dict[str, Any]:
        ...
