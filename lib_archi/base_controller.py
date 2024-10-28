from typing import TypeVar, Generic, Optional, List

from .base_application_service import BaseApplicationService


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
    def __init__(self, app_service: BaseApplicationService[Entity]):
        """Initializes the BaseController with the provided application service.

        Args:
            app_service (BaseApplicationService[Entity]): The application service
                for handling entity operations.
        """
        self.app_service: BaseApplicationService[Entity] = app_service

    def post(self, entity: Entity) -> Optional[Entity]:
        """Handles the creation of a new entity.

        Args:
            entity (Entity): The entity to be created.

        Returns:
            Optional[Entity]: The created entity, or None if creation fails.
        """
        return self.app_service.post(entity)

    def get(self, id: str) -> Entity:
        """Retrieves an entity by its ID.

        Args:
            id (str): The unique identifier of the entity.

        Returns:
            Entity: The entity corresponding to the provided ID.
        """
        return self.app_service.get(id)

    def get_collection(self) -> List[Entity]:
        """Retrieves a collection of all entities.

        Returns:
            List[Entity]: A list of all entities.
        """
        return self.app_service.get_collection()

    def patch(self, entity: Entity) -> Optional[Entity]:
        """Partially updates an existing entity.

            Args:
                entity (Entity): The entity with updated fields.

            Returns:
                Optional[Entity]: The updated entity, or None if the update fails.
            """
        return self.app_service.patch(entity)

    def put(self, entity: Entity) -> Optional[Entity]:
        """Fully updates an existing entity.

        Args:
            entity (Entity): The entity to be fully updated.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        return self.app_service.put(entity)

    def delete(self, id: str)-> Optional[Entity]:
        """Deletes an entity by its ID.

        Args:
            id (str): The unique identifier of the entity to be deleted.

        Returns:
            Optional[Entity]: The deleted entity, or None if deletion fails.
        """
        return self.app_service.delete(id)
