from typing import TypeVar, Generic, Optional
from application_layer.abstractions.applicaiton_interface.icontroller import IController
from lib_archi.base_controller import BaseController
from lib_archi.base_application_service import BaseApplicationService

Entity = TypeVar('Entity')


class Controller(IController, Generic[Entity]):
    """_summary_

    Args:
        IController (_type_): _description_
        Generic (_type_): _description_
    """

    def __init__(self, apps_service: BaseApplicationService[Entity]):
        """_summary_

        Args:
            apps_service (BaseApplicationService[Entity]): _description_
        """
        self.controller = BaseController(apps_service)

    def post(self, entity: Entity):
        """_summary_

        Args:
            entity (Entity): _description_

        Returns:
            _type_: _description_
        """
        return self.controller.post(entity)

    def get(self, id: str) -> Optional[Entity]:
        """_summary_

        Args:
            id (str): _description_

        Returns:
            Optional[Entity]: _description_
        """
        return self.controller.get(id)
