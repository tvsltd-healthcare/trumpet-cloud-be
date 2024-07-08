from typing import TypeVar, Generic, Optional
from application_layer.abstractions.icontroller import IController
from lib_archi.base_controller import BaseController
from lib_archi.base_application_service import BaseApplicationService

Entity = TypeVar('Entity')


class Controller(IController):
    def __init__(self, appService: BaseApplicationService[Entity]):
        self.controller = BaseController(appService)

    def post(self, entity: Entity):
        return self.controller.post(entity.id, entity)

    def get(self, id: str) -> Optional[Entity]:
        return self.controller.get(id)
