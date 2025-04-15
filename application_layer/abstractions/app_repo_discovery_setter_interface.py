from abc import ABC, abstractmethod
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker


class IAppRepoDiscoverySetter(ABC):
    """
    Interface for setting repository invokers based on a specific key.
    This interface is responsible for associating a repository invoker with a given key,
    allowing subsequent retrieval and use of the repository invoker for various operations.
    """

    @abstractmethod
    def set_repo_invoker(self, key: str, repo_invoker: IAppRepoInvoker) -> bool:
        """Sets the repository invoker for a given key.

        Args:
            key (str): A unique identifier or key used to associate with the repository invoker.
            repo_invoker (IAppRepoInvoker): The repository invoker to be associated with the key.

        Returns:
            bool: True if the repository invoker was successfully set, False otherwise.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass
