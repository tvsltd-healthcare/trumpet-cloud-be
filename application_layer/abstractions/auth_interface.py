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
    def read_data(self, token: str) -> Dict:
        pass
