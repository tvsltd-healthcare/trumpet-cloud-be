from abc import ABC, abstractmethod
from typing import Dict


class IAuthenticationHandler(ABC):

    @abstractmethod
    def generate_token(self, params: Dict) -> str:
        pass

    @abstractmethod
    def validate_token(self, token: str) -> bool:
        pass

    @abstractmethod
    def generate_refresh_token(self, params: Dict) -> str:
        pass

    @abstractmethod
    def validate_refresh_token(self, refresh_token: str) -> bool:
        pass
