from abc import ABC, abstractmethod
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker


class IAppRepoDiscoveryGetter(ABC):
    """
    Interface for retrieving repository invokers based on a specific key.
    This interface is responsible for fetching the appropriate repository invoker
    for various repository operations, which can then be used to interact with
    data repositories.
    """

    @abstractmethod
    def get_repo_invoker(self, key: str) -> IAppRepoInvoker:
        """Fetches the repository invoker for a given key.

        Args:
            key (str): A unique identifier or key used to fetch the appropriate repository invoker.

        Returns:
            IAppRepoInvoker: The corresponding repository invoker for performing operations.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass
