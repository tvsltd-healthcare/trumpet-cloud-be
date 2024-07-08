from typing import TypeVar, Generic, Optional
from application_layer.abstractions.icontroller import IController
from lib_archi.base_controller import BaseController
from lib_archi.base_application_service import BaseApplicationService

Entity = TypeVar('Entity')


class Controller(IController, Generic[Entity]):
    def __init__(self, apps_service: BaseApplicationService[Entity]):
        self.controller = BaseController(apps_service)

    def post(self, entity: Entity):
        return self.controller.post(entity.id, entity)

    def get(self, id: str) -> Optional[Entity]:
        return self.controller.get(id)
