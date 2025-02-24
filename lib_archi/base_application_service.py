from .base_repository import BaseRepository
from typing import Any, TypeVar, Generic, Optional, List, Dict


Entity = TypeVar('Entity')


class BaseApplicationService(Generic[Entity]):
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

    def execute_logic_or_repo(self, verb: str, query_or_entity: Any, query: Dict = None):
        logic = self.logic_map.get(verb)

        if logic and callable(logic):
            try:
                return logic(query_or_entity, self.repository)
            
            except Exception as e:
                return None

        # Fallback to repository
        repo_method = getattr(self.repository, verb, None)
        if callable(repo_method):
            if query:
                return repo_method(query_or_entity, query)
            return repo_method(query_or_entity)
        else:
            return None
        
    def get(self, ids: Dict) -> Entity:
        """Retrieves an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity.

        Returns:
            Entity: The entity retrieved from the repository.
        """
        return self.execute_logic_or_repo("get", ids)

    def get_collection(self, ids: Dict) -> List[Entity]:
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
        return self.execute_logic_or_repo("get", ids)

    def post(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Creates a new entity in the repository.

        Args:
            entity (Entity): The entity to be created.

        Returns:
            Optional[Entity]: The created entity, or None if creation fails.
        """
        return self.execute_logic_or_repo("post", ids)

    def put(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Fully updates an existing entity in the repository.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        return self.execute_logic_or_repo("put", ids)

    def patch(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Partially updates an existing entity in the repository.

        Args:
            entity (Entity): The entity with partial updates.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        return self.execute_logic_or_repo("patch", ids)

    def delete(self, ids: Dict) -> Optional[Entity]:
        """Deletes an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity to be deleted.

        Returns:
            Optional[Entity]: The deleted entity, or None if deletion fails.
        """
        return self.execute_logic_or_repo("delete", ids)
