from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from lib_repo_discovery.abstractions.repository_invoker_interface import IRepositoryInvoker
from lib_repo_discovery.repo_discovery import RepoDiscovery


class RepoDiscoveryGetterAdapter(IAppRepoDiscoveryGetter):
    """
    Adapter class for retrieving repository invokers from the RepoDiscovery.
    Implements the IAppRepoDiscoveryGetter interface.
    """

    def __init__(self, repo_discovery: RepoDiscovery):
        """
        Initializes the adapter with the RepoDiscovery instance.

        Args:
            repo_discovery (RepoDiscovery): The concrete RepoDiscovery class instance.
        """
        self.repo_discovery = repo_discovery

    def get_repo_invoker(self, key: str) -> IRepositoryInvoker:
        """Retrieves the repository invoker for the given key."""
        return self.repo_discovery.getRepositoryInvoker(key)
