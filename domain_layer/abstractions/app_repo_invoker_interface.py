from abc import ABC, abstractmethod
from typing import Dict, Optional, Union, List


class IAppRepoInvoker(ABC):
    """
    Interface for repository invoker, providing methods to interact with repository operations.
    This includes fetching, validating, and performing transactional operations on data.
    """

    @abstractmethod
    def get(self, query: Dict, is_collection: bool) -> Union[Optional[object], List[object]]:
        """Retrieves data from the repository based on the given query.

        Args:
            query (Dict): The query parameters used to filter the results.
            is_collection (bool): If True, expects a collection (list) of results; 
                                  otherwise, expects a single object.

        Returns:
            Union[Optional[object], List[object]]: A single object if `is_collection` is False, 
                                                   a list of objects if True, or None if no data is found.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def validate(self, query: Dict, validation_logic: object) -> bool:
        """Validates the given query using the provided validation logic.

        Args:
            query (Dict): The query parameters to validate.
            validation_logic (object): A callable or function used to apply validation rules.

        Returns:
            bool: True if validation passes, False otherwise.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass

    @abstractmethod
    def transact(self, method: str, query: Dict) -> object:
        """Performs a transactional operation based on the given method and query.

        Args:
            method (str): The type of transaction operation (e.g., "CREATE", "UPDATE", "DELETE").
            query (Dict): The query parameters related to the transaction.

        Returns:
            object: The result of the transaction operation.

        Raises:
            NotImplementedError: This method must be implemented in subclasses.
        """
        pass
