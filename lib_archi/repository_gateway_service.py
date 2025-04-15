import traceback
from .base_repository import BaseRepository
from typing import Any, TypeVar, Generic, Optional, List, Dict, Union

Entity = TypeVar('Entity')


class RepositoryGatewayService(Generic[Entity]):
    """
    Gateway service to interact with a repository and optional business logic.
    Allows override of repository methods through custom logic provided via a logic map.
    """

    def __init__(self, repository: BaseRepository[Entity], logic_map: Dict[str, Any] = None):
        """
        Initializes the gateway service.

        Args:
            repository (BaseRepository): The repository instance to delegate default data operations.
            logic_map (Dict[str, Any], optional): A dictionary mapping operation names (verbs) to custom logic.
        """
        self.repository = repository
        self.logic_map = logic_map or {}

    def get_logic(self, verb: str) -> Optional[Any]:
        """
        Retrieves the logic function associated with a given verb from the logic map.

        Args:
            verb (str): The operation key to look up in the logic map.

        Returns:
            Optional[Any]: The logic function if found, otherwise None.
        """
        try:
            logic = self.logic_map.get(verb)
            return logic if logic else None
        except Exception:
            return None

    def get(self, query: Dict, is_collection: bool = False) -> Union[Optional[Entity], List[Entity]]:
        """
        Retrieves an entity or a collection of entities based on the query.

        Args:
            query (Dict): The query parameters to use for fetching data.
            is_collection (bool, optional): If True, fetch a collection; otherwise, fetch a single entity.

        Returns:
            Union[Optional[Entity], List[Entity]]: Result from logic or repository.
        """
        logic = self.get_logic("get_gateway")
        if logic:
            return logic(query, is_collection)
        else:
            return self.repository.get_collection(query) if is_collection else self.repository.get(query)

    def validate(self, query: Dict, validation_logic: object) -> bool:
        """
        Validates the query using the provided validation logic.

        Args:
            query (Dict): The query data to validate.
            validation_logic (object): Custom logic for validation.

        Returns:
            bool: Whether the query is valid.

        Note:
            Placeholder method. To be implemented later with proper validation logic.
        """
        # TODO: later need to decide validation logic with team
        pass

    def transact(self, method: str, data: Dict, query: Dict = None) -> Union[Optional[object], int]:
        """
        Performs a transaction (CRUD operation) using either custom logic or the default repository methods.

        Args:
            method (str): The type of transaction operation (e.g., "POST", "PUT", "DELETE").
            data (Dict): The entity attributes passed as dictionary. e.g. { "first_name": "jhon", "last_name": "doe" }
            query (Dict): The query parameters related to the transaction. e.g. { "id": 7 }

        Returns:
            Union[Optional[object], int]: The object from the operation output 
            or
            int: in case of DELETE operation, the number of items deleted

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
        try:
            logic = self.get_logic("transact")
            query = query or {}

            if logic:
                return logic(method, data)
            else:
                if method == "POST":
                    return self.repository.post(data, query)
                elif method == "DELETE":
                    return self.repository.delete(query)
                elif method == "PUT":
                    return self.repository.put(data, query)
                elif method == "PATCH":
                    return self.repository.patch(data, query)
                else:
                    raise ValueError(f"Unsupported method: {method}")
        except Exception as e:
            print(f"Error processing transaction: {e}")
            traceback.print_exc()
            return None
