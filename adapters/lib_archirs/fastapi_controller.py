import re

from typing import TypeVar, Optional

from application_layer.abstractions.controller_interface import IController
from lib_archi.base_controller import BaseController
from logic_injector.base_logic_injector import BaseLogicInjector

from fastapi import Request


Entity = TypeVar('Entity')
injector = BaseLogicInjector()
BUSINESS_LOGIC_PATHS = r"^/api/studies/\d+/agreements$"


def path_matches(path: str) -> bool:
    """
    Checks if the given path matches the pattern /api/studies/{id}/agreements.

    Args:
        path (str): The URL path to be matched (excluding the base URL).

    Returns:
        bool: True if the path matches the pattern, False otherwise.
    """
    # Todo:: Enhance it for any path matching where we need to inject the business logic

    pattern = BUSINESS_LOGIC_PATHS
    return bool(re.match(pattern, path))


class FastapiController(IController):
    """A FastAPI adapter for handling CRUD operations on entities through a standardized interface.

    This class adapts the `BaseController` to FastAPI's request structure and serves
    as a base for entity CRUD operations by passing relevant path parameters
    to the application layer. The expected path parameters are always in the format:
    
    Example:
        {
            'study_id': 2,
            'id': 5
        }

    Attributes:
        controller (BaseController[Entity]): The base controller that handles entity
            operations at the application layer.

    Args:
        controller (BaseController[Entity]): The controller for managing business logic
            related to the entity.
    """

    def __init__(self, controller: BaseController[Entity]):
        """Initializes the FastAPI controller adapter with the specified base controller.

        Args:
            controller (BaseController[Entity]): The controller handling entity operations.
        """
        self.controller: BaseController[Entity] = controller

    def post(self, entity: Entity, request: Request) -> Optional[Entity]:
        """Handles the creation of a new entity.

        Args:
            entity (Entity): The entity object to be created.
            request (Request): The FastAPI request object containing path parameters.

        Returns:
            Optional[Entity]: The newly created entity, or None if creation fails.
        """
        ids: dict = request.path_params
        result = self.controller.post(entity, ids)

        if path_matches(request.url.path):
            agreement_id = result['data']['id']
            injector.inject_business_logic(entity=entity, entity_id=ids, agreement_id=agreement_id)
        return result

    def get(self, request: Request) -> Entity:
        """Retrieves a specific entity based on path parameters.

        Args:
            request (Request): The FastAPI request object containing path parameters.

        Returns:
            Entity: The retrieved entity.
        """
        ids: dict = request.path_params
        return self.controller.get(ids)

    def get_collection(self, request: Request) -> Entity:
        """Retrieves a collection of entities based on path parameters.

        Args:
            request (Request): The FastAPI request object containing path parameters.

        Returns:
            Entity: A collection of entities matching the request criteria.
        """
        ids: dict = request.path_params
        return self.controller.get_collection(ids)

    def patch(self, entity: Entity, request: Request) -> Optional[Entity]:
        """Partially updates an existing entity.

        Args:
            entity (Entity): The entity object with updated fields.
            request (Request): The FastAPI request object containing path parameters.

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        ids: dict = request.path_params
        return self.controller.patch(entity, ids)

    def put(self, entity: Entity, request: Request) -> Optional[Entity]:
        """Fully replaces an existing entity with new data.

        Args:
            entity (Entity): The entity object containing all required fields.
            request (Request): The FastAPI request object containing path parameters.

        Returns:
            Optional[Entity]: The updated entity, or None if replacement fails.
        """
        ids: dict = request.path_params
        return self.controller.put(entity, ids)

    def delete(self, request: Request) -> Optional[Entity]:
        """Deletes a specific entity based on path parameters.

        Args:
            request (Request): The FastAPI request object containing path parameters.

        Returns:
            Optional[Entity]: Confirmation of the deleted entity, or None if deletion fails.
        """
        ids: dict = request.path_params
        return self.controller.delete(ids)
