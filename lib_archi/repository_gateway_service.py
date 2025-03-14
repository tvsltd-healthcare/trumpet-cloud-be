import traceback
from .base_repository import BaseRepository
from typing import Any, TypeVar, Generic, Optional, List, Dict

Entity = TypeVar('Entity')


class RepositoryGatewayService(Generic[Entity]):
    """Base application service for handling business logic for entities.

    This service layer acts as an intermediary between the controllers and the
    repository. It provides methods to retrieve, create, update, and delete
    entities using the repository.

    Attributes:
        repository (BaseRepository[Entity]): The repository instance responsible
            for CRUD operations on entities.
    """

    def __init__(self, repository: BaseRepository[Entity], logic_map: Dict[str, Any] = None):
        """Initializes the service with a repository instance.

        Args:
            repository (BaseRepository[Entity]): The repository for managing
                entity operations.
        """
        self.repository = repository
        self.logic_map = logic_map or {}

    def inject_logic(self, verb: str ) -> Optional[Any]:
        try:
            logic = self.logic_map.get(verb)
            if logic:
                return logic
            else:
                return None
            
        except Exception as e:
            return None

    def get(self, query: Dict, is_collection: bool) -> Entity:
        """Retrieves an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity.

        Returns:
            Entity: The entity retrieved from the repository.
        """
        logic = self.inject_logic("get")
        if logic:
            return logic(query, is_collection)
        else:
            return self.repository.get(query)

    def validate(self, query: Dict, validation_logic: object) -> bool:
        """Retrieves a collection of all entities.

        Returns:
            List[Entity]: A list of all entities in the repository.

        NOTES::  You can add custom logic or USE CASES here.
        if (Logics.get('get', 'Entity')):
            logic: Logic = Logics.get('get', 'Entity')
            logic(self, id)
        else:
            <something>
        """
        logic = self.inject_logic("validate")
        if logic:
            return logic(query, validation_logic)
        else:
            return self.repository.get_collection(query, validation_logic) #ToDo: Write validation logic later 

    def transact(self, method: str, query: Dict) -> Optional[object]:
        """
        """

        try:
            logic = self.inject_logic("transact")
            ids_dict = {}

            if logic:
                return logic(method, query)
            else:
                if method == "POST":
                    return self.repository.post(query, ids_dict)
                elif method == "DELETE":
                    return self.handle_delete(query)
                elif method == "PUT":
                    return self.handle_put(query)
                elif method == "PATCH":
                    return self.handle_patch(query)
                else:
                    raise ValueError(f"Unsupported method: {method}")
        except Exception as e:
            print(f"Error processing transaction: {e}")
            traceback.print_exc()
            return None