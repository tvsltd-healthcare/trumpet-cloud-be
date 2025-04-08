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
            query (Dict): The query parameters used to filter the results. e.g. { "id": 7 }
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
        """
        """
        pass

    @abstractmethod
    def transact(self, method: str, data: Dict, query: Dict) -> Union[Optional[object], int]:
        """Performs a transactional operation based on the given method and query.

        Args:
            method (str): The type of transaction operation (e.g., "POST", "PUT", "DELETE").
            data (Dict): The entity attributes passed as dictionary. e.g. { "first_name": "jhon", "last_name": "doe" }
            query (Dict): The query parameters related to the transaction. e.g. { "id": 7 }

        Returns:
            object: The result of the transaction operation.
            OR
            int: in case of delete operation, no of item deleted

        Raises:
            NotImplementedError: This method must be implemented in subclasses.

        Usage:
            user_attribute_dict = {
                "first_name": "jhon",
                "last_name": "doe",
                "email": "jhon@tvs.com",
                "password": "string",
                "status": "pending",
                "phone": "0171546253589"
            }

            PUT: 
                user = user_repo_invoker.transact("PUT", data = user_attribute_dict, query = { "id": 7 })
            
            POST:
                user = user_repo_invoker.transact("POST", data = user_attribute_dict)
            
            DELETE:
                user = user_repo_invoker.transact("DELETE", data = {}, query = { "id": 7 })
        """
        pass
