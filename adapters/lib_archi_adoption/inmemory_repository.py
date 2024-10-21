from typing import TypeVar, List, Optional, Dict

from lib_archi.base_entity import BaseEntity
from lib_archi.base_repository import BaseRepository


Entity = TypeVar('Entity', bound=BaseEntity)


class InMemoryRepository(BaseRepository[Entity]):
    """In-memory repository implementing BaseRepository for managing entities.

    This class provides an in-memory implementation of the `BaseRepository`
    interface, allowing CRUD operations on entities stored in a dictionary.
    It is useful for testing or simple applications where persistent storage
    is not needed.

    Attributes:
        entities (Dict[str, Entity]): A dictionary storing the entities, where
            the keys are entity IDs and the values are the entities themselves.
    """

    def __init__(self):
        """Initializes the in-memory repository."""
        self.entities: Dict[str, Entity] = {}

    def get(self, _id: str) -> Optional[Entity]:
        """Retrieve an entity by its unique identifier.

        Args:
            _id (str): The unique identifier of the entity.

        Returns:
            Optional[Entity]: The entity if found, or None if not found.
        """
        return self.entities.get(_id)

    def get_collection(self) -> List[Entity]:
        """Retrieve all entities in the repository.

        Returns:
            List[Entity]: A list of all entities in the repository.
        """
        return list(self.entities.values())

    def post(self, entity: Entity) -> Optional[Entity]:
        """Create a new entity if it does not already exist.

        Args:
            entity (Entity): The entity to be created.

        Returns:
            Optional[Entity]: The newly created entity.

        Raises:
            ValueError: If an entity with the same ID already exists.
        """
        if entity._id not in self.entities:
            self.entities[entity._id] = entity
            return entity

        raise ValueError(f"Entity with id {entity.id} already exists")

    def update(self, entity: Entity) -> Optional[Entity]:
        """Update an existing entity in the repository.

        Args:
            entity (Entity): The entity with updated information.

        Returns:
            Optional[Entity]: The updated entity.

        Raises:
            ValueError: If the entity does not exist in the repository.
        """
        if entity._id in self.entities:
            self.entities[entity._id] = entity
            return entity

        raise ValueError(f"Entity with id {entity._id} does not exist")

    def delete(self, _id: str) -> Optional[Entity]:
        """Delete an entity by its unique identifier.

        Args:
            _id (str): The unique identifier of the entity to be deleted.

        Returns:
            Optional[Entity]: The deleted entity, or None if no such entity exists.
        """
        entity = self.entities.pop(_id, None)
        return entity

    def patch(self, entity: Entity) -> Optional[Entity]:
        """Patch an existing entity with partial updates.

        Args:
            entity (Entity): The entity with partial updates.

        Returns:
            Optional[Entity]: The updated entity.

        Raises:
            ValueError: If the entity does not exist in the repository.
        """
        existing_entity = self.get(entity._id)
        if not existing_entity:
            raise ValueError(f"Entity with id {entity._id} does not exist")

        # Update only the attributes provided
        for attr, value in entity.__dict__.items():
            if value is not None:
                setattr(existing_entity, attr, value)

        self.entities[entity._id] = existing_entity
        return existing_entity

    def put(self, entity: Entity) -> Optional[Entity]:
        """Put an existing entity with full updates.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity.

        Raises:
            ValueError: If the entity does not exist in the repository.
        """
        if entity._id in self.entities:
            self.entities[entity._id] = entity
            return entity

        raise ValueError(f"Entity with id {entity._id} does not exist")
