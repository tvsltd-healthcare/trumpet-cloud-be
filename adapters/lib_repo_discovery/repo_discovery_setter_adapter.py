from application_layer.abstractions.app_repo_discovery_setter_interface import IAppRepoDiscoverySetter
from lib_repo_discovery.abstractions.repository_invoker_interface import IRepositoryInvoker
from lib_repo_discovery.repo_discovery import RepoDiscovery


class RepoDiscoverySetterAdapter(IAppRepoDiscoverySetter):
    """
    Adapter class for setting repository invokers into the RepoDiscovery.
    Implements the IAppRepoDiscoverySetter interface.
    """

    def __init__(self, repo_discovery: RepoDiscovery):
        """
        Initializes the adapter with the RepoDiscovery instance.

        Args:
            repo_discovery (RepoDiscovery): The concrete RepoDiscovery class instance.
        """
        self.repo_discovery = repo_discovery

    def set_repo_invoker(self, key: str, repo_invoker: IRepositoryInvoker) -> None:
        """Sets the repository invoker for a given key."""
        self.repo_discovery.addToRepositoryInvokerRegistry(key, repo_invoker)
