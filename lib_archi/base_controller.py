import uuid
from datetime import datetime

from typing import TypeVar, Generic, Optional, List
from .base_application_service import BaseApplicationService
from application_layer.abstractions.response_interface import IResponseHandler

Entity = TypeVar('Entity')


class BaseController(Generic[Entity]):
    """A generic base controller for handling CRUD operations on entities.

    This class defines the standard CRUD (Create, Read, Update, Delete) methods
    for an entity by utilizing the corresponding application service.

    Attributes:
        app_service (BaseApplicationService[Entity]): The application service that
            performs operations on the entity.

    Args:
        app_service (BaseApplicationService[Entity]): The service for handling
            the business logic related to the entity.
    """

    def __init__(self, app_service: BaseApplicationService[Entity], response_handler: IResponseHandler):
        """Initializes the BaseController with the provided application service.

        Args:
            app_service (BaseApplicationService[Entity]): The application service
                for handling entity operations.
        """
        self.app_service: BaseApplicationService[Entity] = app_service
        self.response_handler: IResponseHandler = response_handler

    def post(self, entity: Entity) -> Optional[Entity]:
        """Handles the creation of a new entity.

        Args:
            entity (Entity): The entity to be created.

        Returns:
            Optional[Entity]: The created entity, or None if creation fails.
        """
        try:
            entity = self._refine_store_date(entity)
            entity = self._add_uniq_id(entity)
            created_entity = self.app_service.post(entity)
            return self.response_handler.resource_detail("Entity created successfully", data=created_entity, status_code=201)
        except Exception as e:
            return self.response_handler.error_response(f"{str(e)}", 400)

    def get(self, id: int) -> Entity:
        """Retrieves an entity by its ID.

        Args:
            id (str): The unique identifier of the entity.

        Returns:
            Entity: The entity corresponding to the provided ID.
        """
        try:
            get_entity = self.app_service.get(id)
            
            if get_entity is None or not bool(get_entity):
                return self.response_handler.error_response("item not found", 404)
            
            return self.response_handler.resource_detail("Entity retrieved successfully", data=get_entity)
        except Exception as e:
            return self.response_handler.error_response(f"{str(e)}", 400)

    def get_collection(self) -> Entity:
        """Retrieves a collection of all entities.

        Returns:
            List[Entity]: A list of all entities.
        """
        try:
            entities = self.app_service.get_collection()
            return self.response_handler.resource_list("Entities retrieved successfully", data=entities)
        except Exception as e:
            return self.response_handler.error_response(f"{str(e)}", 400)

    def patch(self, entity: Entity) -> Optional[Entity]:
        """Partially updates an existing entity.

            Args:
                entity (Entity): The entity with updated fields.

            Returns:
                Optional[Entity]: The updated entity, or None if the update fails.
            """
        try:
            entity = self._refine_store_date(entity)
            updated_entity = self.app_service.patch(entity)
            return self.response_handler.resource_detail("Entity updated successfully", data=updated_entity)
        except Exception as e:
            return self.response_handler.error_response(f"{str(e)}", 400)

    def put(self, entity: Entity) -> Optional[Entity]:
        """Fully updates an existing entity.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        try:
            entity = self._refine_store_date(entity)
            updated_entity = self.app_service.put(entity)
            return self.response_handler.resource_detail("Entity fully updated", data=updated_entity)
        except Exception as e:
            return self.response_handler.error_response(f"{str(e)}", 400)

    def delete(self, id: str) -> Optional[Entity]:
        """Deletes an entity by its ID.

        Args:
            id (str): The unique identifier of the entity to be deleted.

        Returns:
            Optional[Entity]: The deleted entity, or None if deletion fails.
        """
        try:
            deleted_entity = self.app_service.delete(id)
            return self.response_handler.resource_detail("Entity deleted successfully")
        except Exception as e:
            return self.response_handler.error_response(f"{str(e)}", 400)
        
    def _refine_store_date(self, entity: Entity) -> Entity:
        if not hasattr(entity, 'updated_at') or entity.updated_at is None:
            entity.updated_at = datetime.now()

        if not hasattr(entity, 'created_at') or entity.created_at is None:
            entity.created_at = datetime.now()

        return entity
    
    def _add_uniq_id(self, entity: Entity) -> Entity:
        entity.id = str(uuid.uuid4())
        return entity
