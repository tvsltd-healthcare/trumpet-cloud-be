from abc import ABC, abstractmethod

class IRepositoryInvoker(ABC):
    """
    Interface for repository invokers. All repository invokers should implement
    the methods for getting data, validating it, and performing transactions.
    """

    @abstractmethod
    def get(self) -> object:
        """Method to retrieve data from the repository."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Method to validate data in the repository."""
        pass

    @abstractmethod
    def transact(self) -> object:
        """Method to perform transactions with the repository."""
        pass
