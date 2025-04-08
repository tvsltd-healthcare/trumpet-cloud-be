from typing import List, Optional, Union
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from lib_archi.repository_gateway_service import RepositoryGatewayService

class RepoDirectInvokerAdapter(IAppRepoInvoker):
    """
    Adapter class that implements IAppRepoInvoker and interacts directly with a given repository invoker.
    This class allows invoking methods like get(), validate(), and transact() on a specific IRepositoryInvoker.
    """

    def __init__(self, repo_gateway: RepositoryGatewayService):
        """
        Initializes the adapter with the given repository invoker.

        Args:
            repo_gateway (IRepositoryInvoker): The repository invoker that will be used to execute operations.
        """
        self.repo_gateway = repo_gateway

    def get(self, query: dict, is_collection: bool = False) -> Union[Optional[object], List[object]]:
        """
        Invokes the get method on the wrapped repository invoker.

        Args:
            query (Dict): The query parameters used to filter the results. e.g. { "id": 7 }
            is_collection (bool): A flag to indicate whether a collection or a single entity is expected.

        Returns:
            object: The result returned from the get method of the repository invoker.
        """
        return self.repo_gateway.get(query, is_collection)

    def validate(self, query: dict, validation_logic: object) -> bool:
        """
        Invokes the validate method on the wrapped repository invoker.

        Args:
            query (dict): The query to be validated.
            validation_logic (object): The validation logic to be applied.

        Returns:
            bool: The result of the validation operation.
        """
        return self.repo_gateway.validate(query, validation_logic)

    def transact(self, method: str, data: dict, query: dict = None) -> Union[Optional[object], int]:
        """
        Invokes the transact method on the wrapped repository invoker.

        Args:
            method (str): The type of transaction operation (e.g., "POST", "PUT", "DELETE").
            data (Dict): The entity attributes passed as dictionary. e.g. { "first_name": "jhon", "last_name": "doe" }
            query (Dict): The query parameters related to the transaction. e.g. { "id": 7 }

        Returns:
            object: The result of the transaction.
            OR
            int: in case of DELETE operation, the number of items deleted
        """
        return self.repo_gateway.transact(method, data, query)
