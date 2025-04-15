from abc import ABC, abstractmethod
from lib_repo_discovery.abstractions.repository_invoker_interface import IRepositoryInvoker

class IRepositoryInvokerRegistration(ABC):
    """
    Interface for registering repository invokers in a registry. This interface
    allows adding invokers to a repository registry and retrieving them using keys.
    """

    @abstractmethod
    def addToRepositoryInvokerRegistry(self, key: str, repo_invoker: IRepositoryInvoker) -> bool:
        """Adds a repository invoker to the registry."""
        pass
