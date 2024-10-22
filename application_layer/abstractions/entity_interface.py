from abc import ABC, abstractmethod
from typing import Dict


class IEntityGenerator(ABC):
    @abstractmethod
    def create(self, entity_name: str, input_dict: Dict):
        pass

    @abstractmethod
    def validate(self, entity_name: str, data: Dict):
        pass
