from typing import TypeVar, Generic, Optional
from .base_application_service import BaseApplicationService

Entity = TypeVar('Entity')


class BaseController(Generic[Entity]):
    """_summary_

    Args:
        Generic (_type_): _description_
    """

    def __init__(self, app_service: BaseApplicationService[Entity]):
        """_summary_

        Args:
            app_service (BaseApplicationService[Entity]): _description_
        """
        self.app_service: BaseApplicationService[Entity] = app_service

    def post(self, entity: Entity):
        """_summary_

        Args:
            entity (Entity): _description_

        Returns:
            _type_: _description_
        """
        return self.app_service.post(entity.id, entity)

    def get(self, _id: str) -> Optional[Entity]:
        """_summary_

        Args:
            id (str): _description_

        Returns:
            Optional[Entity]: _description_
        """
        return self.app_service.get(_id)


    def get_collection(self) -> Optional[Entity]:
        """_summary_

        Args:
            id (str): _description_

        Returns:
            Optional[Entity]: _description_
        """
        return self.app_service.get_collection()
