from .base_repository import BaseRepository
from typing import TypeVar, Generic, Optional, List


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

    def __init__(self, repository: BaseRepository[Entity]):
        """Initializes the service with a repository instance.

        Args:
            repository (BaseRepository[Entity]): The repository for managing
                entity operations.
        """
        self.repository = repository

    def get(self, id: int) -> Entity:
        """Retrieves an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity.

        Returns:
            Entity: The entity retrieved from the repository.
        """
        return self.repository.get(id)

    def get_collection(self) -> List[Entity]:
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
        return self.repository.get_collection()

    def post(self, entity: Entity) -> Optional[Entity]:
        """Creates a new entity in the repository.

        Args:
            entity (Entity): The entity to be created.

        Returns:
            Optional[Entity]: The created entity, or None if creation fails.
        """
        return self.repository.post(entity)

    def put(self, entity: Entity) -> Optional[Entity]:
        """Fully updates an existing entity in the repository.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        return self.repository.put(entity)

    def patch(self, entity: Entity) -> Optional[Entity]:
        """Partially updates an existing entity in the repository.

        Args:
            entity (Entity): The entity with partial updates.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        return self.repository.patch(entity)

    def delete(self, id: str) -> Optional[Entity]:
        """Deletes an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity to be deleted.

        Returns:
            Optional[Entity]: The deleted entity, or None if deletion fails.
        """
        return self.repository.delete(id)
