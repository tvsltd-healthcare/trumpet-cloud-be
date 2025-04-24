from lib_archi.abstractions.request_interface import IRequest
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

    def inject_logic(self, verb: str ) -> Optional[Any]:
        try:
            logic = self.logic_map.get(verb)
            if logic:
                return logic
            else:
                return None
            
        except Exception as e:
            return None

    def get(self, request: IRequest) -> Entity:
        """Retrieves an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity.

        Returns:
            Entity: The entity retrieved from the repository.
        """
        logic = self.inject_logic("get")
        if logic:
            return logic(request, self.repository)
        else:
            ids = request.get_path_params()
            return self.repository.get(ids)

    def get_collection(self, request: IRequest) -> List[Entity]:
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
        logic = self.inject_logic("get_collection")
        if logic:
            return logic(request, self.repository)
        else:
            ids = request.get_path_params()
            return self.repository.get_collection(ids)

    def post(self, entity: Entity, request: IRequest) -> Optional[Entity]:
        """Creates a new entity in the repository.

        Args:
            entity (Entity): The entity to be created.

        Returns:
            Optional[Entity]: The created entity, or None if creation fails.
        """
        logic = self.inject_logic("post")
        if logic:
            return logic(request, self.repository, entity)
        else:
            ids = request.get_path_params()
            return self.repository.post(entity, ids)

    def put(self, entity: Entity, request: IRequest) -> Optional[Entity]:
        """Fully updates an existing entity in the repository.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        logic = self.inject_logic("put")
        if logic:
            return logic(request, self.repository, entity)
        else:
            ids = request.get_path_params()
            return self.repository.put(entity, ids)

    def patch(self, entity: Entity, request: IRequest) -> Optional[Entity]:
        """Partially updates an existing entity in the repository.

        Args:
            entity (Entity): The entity with partial updates.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        logic = self.inject_logic("patch")
        if logic:
            return logic(request, self.repository, entity)
        else:
           ids = request.get_path_params()
           return self.repository.patch(entity, ids)

    def delete(self, request: IRequest) -> Optional[Entity]:
        """Deletes an entity by its unique identifier.

        Args:
            id (str): The unique identifier of the entity to be deleted.

        Returns:
            Optional[Entity]: The deleted entity, or None if deletion fails.
        """
        logic = self.inject_logic("patch")
        if logic:
            return logic(request, self.repository)
        else:
           ids = request.get_path_params()
           return self.repository.delete(ids)
