from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

class IRepositoryInvoker(ABC):
    """
    Interface for repository invokers. All repository invokers should implement
    the methods for getting data, validating it, and performing transactions.
    """

    @abstractmethod
    def get(self, query: Dict, is_collection: bool = False) -> Union[Optional[object], List[object]]:
        """Method to retrieve data from the repository."""
        pass

    @abstractmethod
    def validate(self, query: Dict, validation_logic: object) -> bool:
        """Method to validate data in the repository."""
        pass

    @abstractmethod
    def transact(self, method: str, data: Dict, query: Dict = None) -> object:
        """Method to perform transactions with the repository."""
        pass
