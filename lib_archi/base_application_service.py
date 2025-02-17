from .base_repository import BaseRepository
from typing import TypeVar, Generic, Optional, List, Dict


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

    def __init__(self, repository: BaseRepository[Entity], logic_map: Dict = None):
        """Initializes the service with a repository instance.

        Args:
            repository (BaseRepository[Entity]): The repository for managing
                entity operations.
        """
        self.repository = repository
        print('logic_map, BaseApplicationService', logic_map)
        self.logic_map = logic_map or {}

    def get(self, ids: Dict) -> Entity:
        """Retrieves an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity.

        Returns:
            Entity: The entity retrieved from the repository.
        """
        if self.logic_map.get("get"):
            return self.logic_map["get"]()
        return self.repository.get(ids)

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
        print('===========<>Execute logics', self.logic_map)
        if self.logic_map.get("get"):
            return self.logic_map["get"]()
        return self.repository.get_collection(ids)

    def post(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Creates a new entity in the repository.

        Args:
            entity (Entity): The entity to be created.

        Returns:
            Optional[Entity]: The created entity, or None if creation fails.
        """
        if self.logic_map.get("put"):
            return self.logic_map["put"]()
        return self.repository.post(entity, ids)

    def put(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Fully updates an existing entity in the repository.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        return self.repository.put(entity, ids)

    def patch(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Partially updates an existing entity in the repository.

        Args:
            entity (Entity): The entity with partial updates.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        if self.logic_map.get("patch"):
            return self.logic_map["patch"]()
        return self.repository.patch(entity, ids)

    def delete(self, ids: Dict) -> Optional[Entity]:
        """Deletes an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity to be deleted.

        Returns:
            Optional[Entity]: The deleted entity, or None if deletion fails.
        """
        return self.repository.delete(ids)
