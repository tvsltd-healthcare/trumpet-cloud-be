from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Union

from .base_entity import BaseEntity


Entity = TypeVar('Entity', bound=BaseEntity)


class BaseRepository(ABC, Generic[Entity]):
    """Abstract base class for a repository to manage CRUD operations on entities.

    This class defines the interface for a repository that handles data access
    for entities, including methods for retrieving, creating, updating, and
    deleting entities. Concrete implementations of this class must provide
    implementations for all methods.

    Type Parameters:
        Entity: The entity type that the repository will manage. Must be a subclass
        of `BaseEntity`.
    """

    @abstractmethod

    def get(self, ids: Dict) -> Entity:
        """Retrieve an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity to retrieve.

        Returns:
            Entity: The entity corresponding to the provided ID.
        """
        pass

    @abstractmethod
    def get_collection(self, ids: Dict) -> List[Entity]:
        """Retrieve all entities.

        Returns:
            List[Entity]: A list of all entities managed by the repository.
        """
        pass

    @abstractmethod
    def post(self, entity: Union[Entity, dict], ids: Dict) -> Optional[Entity]:
        """Create a new entity.

        Args:
            entity (Entity): The entity to create.

        Returns:
            Optional[Entity]: The created entity, or None if creation fails.
        """
        pass

    @abstractmethod
    def delete(self, ids: Dict) -> Optional[Entity]:
        """Delete an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity to delete.

        Returns:
            Optional[Entity]: The deleted entity, or None if deletion fails.
        """
        pass

    @abstractmethod
    def patch(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Patch an existing entity with partial updates.

        Args:
            entity (Entity): The entity with partial updates.

        Returns:
            Optional[Entity]: The patched entity, or None if the patch fails.
        """
        pass

    @abstractmethod
    def put(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Put an existing entity with full updates or changes.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        pass
