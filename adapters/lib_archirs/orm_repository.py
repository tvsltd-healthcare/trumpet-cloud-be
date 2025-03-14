from typing import TypeVar, List, Optional, Dict, Type, Union
from datetime import datetime

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

    def get(self, ids: Dict) -> Optional[Entity]:
        """Retrieve an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity.

        Returns:
            Optional[Entity]: The entity if found, or None if not found.
        """

        filter_string = " AND ".join(f"{key}={value}" for key, value in ids.items())

        query_dict = {
            "model": self.orm_model_key,
            "filter": filter_string,
        }

        print(filter_string)

        result = self.orm.query(query_dict)

        return result[0] if isinstance(result, list) and len(result) == 1 else result


    def get_collection(self, ids: Dict) -> List[Entity]:
        """Retrieve all entities in the repository.

        Returns:
            List[Entity]: A list of all entities in the repository.
        """
        filter_string = " AND ".join(f"{key}={value}" for key, value in ids.items())

        query_dict = {
            "model": self.orm_model_key,
            "filter": filter_string,
        }

        return self.orm.query(query_dict)

    def post(self, entity:  Union[Entity, dict], ids: Dict) -> Optional[Entity]:
        """Create a new entity if it does not already exist.

        Args:
            entity (Entity): The entity to be created.

        Returns:
            Optional[Entity]: The newly created entity.

        Raises:
            ValueError: If an entity with the same ID already exists.
        """
        entity_dict = entity if isinstance(entity, dict) else vars(entity)
        entity_dict.pop('id', None)

        if ids is not None:
            for key, value in ids.items():
                entity_dict[key] = value
        
        insert_dict = {
            "model": self.orm_model_key,
            'attributes': entity_dict
        }

        result = self.orm.insert(insert_dict)

        return result[0] if isinstance(result, list) and len(result) == 1 else result
        

    def update(self, entity: Entity, ids: Dict) -> Optional[Entity]:
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

        filter_string = " AND ".join(f"{key}={value}" for key, value in ids.items())

        entity_dict = {key: value for key, value in entity_dict.items() if value is not None}

        if ids is not None:
            for key, value in ids.items():
                entity_dict[key] = value

        update_dict = {
            "model": self.orm_model_key,
            "filter": filter_string,
            'attributes': entity_dict
        }

        result = self.orm.update(update_dict)
        final_result = result[0] if isinstance(result, list) and len(result) == 1 else result

        if not final_result:
            raise Exception("Operaion Failed")
        
        return final_result

    def delete(self, ids: Dict) -> Optional[Entity]:
        """Delete an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity to be deleted.

        Returns:
            Optional[Entity]: The deleted entity, or None if no such entity exists.
        """

        filter_string = " AND ".join(f"{key}={value}" for key, value in ids.items())

        delete_dict = {
            "model": self.orm_model_key,
            "filter": filter_string,
        }

        result = self.orm.delete(delete_dict)

        if result in {None, 0, '0'}:
            raise Exception("Operaion Failed")
        
        return result


    def patch(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Patch an existing entity with partial updates.

        Args:
            entity (Entity): The entity with partial updates.

        Returns:
            Optional[Entity]: The updated entity.

        Raises:
            ValueError: If the entity does not exist in the repository.
        """
        return self.update(entity, ids)

    def put(self, entity: Entity, ids: Dict) -> Optional[Entity]:
        """Put an existing entity with full updates.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity.

        Raises:
            ValueError: If the entity does not exist in the repository.
        """
        return self.update(entity, ids)

    def _pascal_to_singular_snake(self, pascal_str: str) -> str:
        # Convert PascalCase to snake_case using stringcase
        snake_case = stringcase.snakecase(pascal_str)

        # Initialize inflect engine for singularization
        inflect_engine = inflect.engine()

        # Convert plural to singular
        singular_snake_case = inflect_engine.singular_noun(snake_case) or snake_case

        return singular_snake_case
