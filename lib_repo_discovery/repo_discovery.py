from typing import Dict, Optional
from lib_repo_discovery.abstractions.repository_invoker_registration_interface import IRepositoryInvokerRegistration
from lib_repo_discovery.abstractions.repository_invoker_interface import IRepositoryInvoker


class RepoDiscovery(IRepositoryInvokerRegistration):
    """
    Concrete class implementing IRepositoryInvokerRegistration interface.
    This class manages the registry of repository invokers against unique keys.
    """

    def __init__(self):
        self.registry: Dict[str, IRepositoryInvoker] = {}

    def addToRepositoryInvokerRegistry(self, key: str, repo_invoker: IRepositoryInvoker) -> bool:
        """Adds a repository invoker to the registry."""
        if key in self.registry:
            return False  # Key already exists
        self.registry[key] = repo_invoker
        return True

    def getRepositoryInvoker(self, key: str) -> Optional[IRepositoryInvoker]:
        """Retrieves a repository invoker from the registry by key."""
        return self.registry.get(key, None)
