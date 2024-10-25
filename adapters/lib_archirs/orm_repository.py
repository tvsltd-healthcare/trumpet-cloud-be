from typing import TypeVar, List, Optional, Dict, Type

import stringcase
import inflect

from lib_archi.base_entity import BaseEntity
from lib_archi.base_repository import BaseRepository

from adapters.wrap_orm_adapters.orm_adapter import OrmAdapter
from application_layer.abstractions.orm_interface import IOrm

from adapters.response_adapters.response_handler import ResponseHandler

Entity = TypeVar('Entity', bound=BaseEntity)


class OrmRepository(BaseRepository[Entity]):
    """In-memory repository implementing BaseRepository for managing entities.

    This class provides an in-memory implementation of the `BaseRepository`
    interface, allowing CRUD operations on entities stored in a dictionary.
    It is useful for testing or simple applications where persistent storage
    is not needed.

    Attributes:
        entities (Dict[str, Entity]): A dictionary storing the entities, where
            the keys are entity IDs and the values are the entities themselves.
    """
    entity_type: Type[BaseEntity] = None # Class-level attribute to store the entity type
    
    def __init__(self, orm: IOrm):
        """Initializes the in-memory repository."""
        self.orm_model_key = self._pascal_to_singular_snake(self.entity_type.__name__)
        self.orm = orm
        self.response = ResponseHandler()

    @classmethod
    def __class_getitem__(cls, entity_type: Type[Entity]):
        """Sets the entity type when accessing via indexing, e.g. InMemoryRepository[Entity]."""
        cls.entity_type = entity_type
        return cls

    def get(self, id: str) -> Optional[Entity]:
        """Retrieve an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity.

        Returns:
            Optional[Entity]: The entity if found, or None if not found.
        """
        query_dict = {
            "model": self.orm_model_key,
            "filter": f"id={id}",
        }

        return self.orm.query(query_dict)

    def get_collection(self) -> List[Entity]:
        """Retrieve all entities in the repository.

        Returns:
            List[Entity]: A list of all entities in the repository.
        """
        query_dict = {
            "model": self.orm_model_key,
        }

        return self.orm.query(query_dict)

    def post(self, entity: Entity) -> Optional[Entity]:
        """Create a new entity if it does not already exist.

        Args:
            entity (Entity): The entity to be created.

        Returns:
            Optional[Entity]: The newly created entity.

        Raises:
            ValueError: If an entity with the same ID already exists.
        """
        insert_dict = {
                "model": self.orm_model_key,
                'attributes': vars(entity)
            }

        result_list = self.orm.insert(insert_dict)
        print(result_list)
        return result_list
        # try:
        #     insert_dict = {
        #         "model": self.orm_model_key,
        #         'attributes': vars(entity)
        #     }

        #     result_list = self.orm.insert(insert_dict)
        #     return self.response.resource_list(message = 'Success', data=result_list, status_code=201)
        # except Exception as e:
        #     print(e)
        #     return self.response.error_response(message = f'{e}')
        

    def update(self, entity: Entity) -> Optional[Entity]:
        """Update an existing entity in the repository.

        Args:
            entity (Entity): The entity with updated information.

        Returns:
            Optional[Entity]: The updated entity.

        Raises:
            ValueError: If the entity does not exist in the repository.
        """
        entity_dict = vars(entity)
        entity_id = entity_dict.get('id')

        update_dict = {
            "model": self.orm_model_key,
            "filter": f"id={entity_id}",
            'attributes': vars(entity)
        }

        return self.orm.update(update_dict)

    def delete(self, id: str) -> Optional[Entity]:
        """Delete an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity to be deleted.

        Returns:
            Optional[Entity]: The deleted entity, or None if no such entity exists.
        """
        delete_dict = {
            "model": self.orm_model_key,
            "filter": f"id={id}",
        }

        return self.orm.delete(delete_dict)


    def patch(self, entity: Entity) -> Optional[Entity]:
        """Patch an existing entity with partial updates.

        Args:
            entity (Entity): The entity with partial updates.

        Returns:
            Optional[Entity]: The updated entity.

        Raises:
            ValueError: If the entity does not exist in the repository.
        """
        entity_dict = vars(entity)
        entity_id = entity_dict.pop('id')

        update_dict = {
            "model": self.orm_model_key,
            "filter": f"id={entity_id}",
            'attributes': vars(entity)
        }

        return self.orm.update(update_dict)

    def put(self, entity: Entity) -> Optional[Entity]:
        """Put an existing entity with full updates.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity.

        Raises:
            ValueError: If the entity does not exist in the repository.
        """
        entity_dict = vars(entity)
        entity_id = entity_dict.pop('id')

        update_dict = {
            "model": self.orm_model_key,
            "filter": f"id={entity_id}",
            'attributes': vars(entity)
        }

        return self.orm.update(update_dict)

    def _pascal_to_singular_snake(self, pascal_str: str) -> str:
        # Convert PascalCase to snake_case using stringcase
        snake_case = stringcase.snakecase(pascal_str)

        # Initialize inflect engine for singularization
        inflect_engine = inflect.engine()

        # Convert plural to singular
        singular_snake_case = inflect_engine.singular_noun(snake_case) or snake_case

        return singular_snake_case
