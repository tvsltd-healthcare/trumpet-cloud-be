import re
import uuid
from datetime import datetime

from typing import TypeVar, Generic, Optional, Dict

from lib_archi.abstractions.request_interface import IRequest
from lib_archi.utils.enforce_request_interface import enforce_request_type
from .base_application_service import BaseApplicationService
from application_layer.abstractions.response_interface import IResponseHandler
from logic_injector.base_logic_injector import BaseLogicInjector

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

    @enforce_request_type()
    def post(self, request: IRequest, entity: Entity) -> Optional[Entity]:
        """Handles the creation of a new entity.

        Args:
            entity (Entity): The entity to be created.
            ids (Dict): dictionary of id and parent ids.  
                Ex: {
                    'study_id': 2,
                    'id': 5
                }

        Returns:
            Optional[Entity]: The created entity, or None if creation fails.
        """
        try:
            entity = self._refine_store_date(entity, request)
            entity = self._add_uniq_id(entity)
            created_entity = self.app_service.post(entity, request)

            # todo: for now turning off the start train trigger. will add it to different endpoint
            # if path_matches(request.get_path()):
            #     ids: dict = request.get_path_params()
            #     agreement_id = created_entity['id']
            #     injector.inject_business_logic(entity=entity, entity_id=ids, agreement_id=agreement_id)

            return self.response_handler.generate_response("Entity created successfully", data=created_entity,
                                                           status_code=201)
        except Exception as e:
            return self.response_handler.generate_response(f"{str(e)}", 400)

    @enforce_request_type()
    def get(self, request: IRequest) -> Entity:
        """Retrieves an entity by its ID.

        Args:
            ids (Dict): dictionary of id and parent ids.  
                Ex: {
                    'study_id': 2,
                    'id': 5
                }

        Returns:
            Entity: The entity corresponding to the provided ID.
        """
        try:
            get_entity = self.app_service.get(request)

            if get_entity is None or not bool(get_entity):
                return self.response_handler.generate_response("item not found", 404)

            return self.response_handler.generate_response("Entity retrieved successfully", data=get_entity)
        except Exception as e:
            return self.response_handler.generate_response(f"{str(e)}", 400)

    @enforce_request_type()
    def get_collection(self, request: IRequest) -> Entity:
        """Retrieves a collection of all entities.

        Args:
            ids (Dict): dictionary of id and parent ids.  
                Ex: {
                    'study_id': 2,
                    'id': 5
                }

        Returns:
            List[Entity]: A list of all entities.
        """
        try:
            entities = self.app_service.get_collection(request)
            return self.response_handler.generate_response("Entities retrieved successfully", data=entities)
        except Exception as e:
            return self.response_handler.generate_response(f"{str(e)}", 400)

    @enforce_request_type()
    def patch(self, request: IRequest, entity: Entity) -> Optional[Entity]:
        """Partially updates an existing entity.

            Args:
                entity (Entity): The entity with updated fields.
                ids (Dict): dictionary of id and parent ids.  
                    Ex: {
                        'study_id': 2,
                        'id': 5
                    }

            Returns:
                Optional[Entity]: The updated entity, or None if the update fails.
            """
        try:
            entity = self._refine_store_date(entity, request)

            updated_entity = self.app_service.patch(entity, request)
            return self.response_handler.generate_response("Entity updated successfully", data=updated_entity)
        except Exception as e:
            return self.response_handler.generate_response(f"{str(e)}", 400)

    @enforce_request_type()
    def put(self, request: IRequest, entity: Entity) -> Optional[Entity]:
        """Fully updates an existing entity.

        Args:
            entity (Entity): The entity to be fully updated.
            ids (Dict): dictionary of id and parent ids.  
                    Ex: {
                        'study_id': 2,
                        'id': 5
                    }

        Returns:
            Optional[Entity]: The updated entity, or None if the update fails.
        """
        try:
            if self._all_attrs_not_provided(entity):
                raise ValueError("PUT request requires all attributes to be provided.")

            ids = request.get_path_params()

            entity = self._refine_store_date(entity, request)
            updated_entity = self.app_service.put(entity, request)
            return self.response_handler.generate_response("Entity fully updated", data=updated_entity)
        except Exception as e:
            return self.response_handler.generate_response(f"{str(e)}", 400)

    @enforce_request_type()
    def delete(self, request: IRequest) -> Optional[Entity]:
        """Deletes an entity by its ID.

        Args:
            ids (Dict): dictionary of id and parent ids.  
                    Ex: {
                        'study_id': 2,
                        'id': 5
                    }

        Returns:
            Optional[Entity]: The deleted entity, or None if deletion fails.
        """
        ids = request.get_path_params()

        try:
            for key, value in ids.items():
                if not value:
                    raise ValueError(f"The value for '{key}' is null or empty.")

            deleted_entity = self.app_service.delete(ids)
            return self.response_handler.generate_response("Entity deleted successfully")
        except Exception as e:
            return self.response_handler.generate_response(f"{str(e)}", 400)

    def _refine_store_date(self, entity: Entity, request: IRequest) -> Entity:
        user_id = request.get_request().scope['state']['user_id'] if request.get_request().scope['state']['user_id'] is not None else None
        if request.get_method_name() == 'POST':
            if not hasattr(entity, 'created_at') or entity.created_at is None:
                entity.created_at = datetime.now()
            if not hasattr(entity, 'created_by') or entity.created_by is None:
                entity.created_by = user_id

        if request.get_method_name() == 'PUT' or request.get_method_name() == 'PATCH':
            if not hasattr(entity, 'updated_at') or entity.updated_at is None:
                entity.updated_at = datetime.now()
            if not hasattr(entity, 'updated_by') or entity.updated_by is None:
                entity.updated_by = user_id

        return entity

    def _add_uniq_id(self, entity: Entity) -> Entity:
        entity.id = str(uuid.uuid4())
        return entity

    def _all_attrs_not_provided(self, entity: Entity) -> bool:
        # Convert the entity to a dictionary if it has a __dict__ attribute.
        entity_dict = entity.__dict__ if hasattr(entity, "__dict__") else entity

        # Iterate over all keys and values except `id`
        for key, value in entity_dict.items():
            if key != 'id' and (value is None or value == '' or value == '0'):
                return True

        return False
