from lib_archi.base_application_service import BaseApplicationService
from typing import TypeVar, Generic, Optional

Entity = TypeVar('Entity')


class IController(Generic[Entity]):
    def __init__(self, appService: BaseApplicationService[Entity]):
        self.appService: BaseApplicationService[Entity] = appService

    def post(self, entity: Entity):
        pass

    def get(self, id: str) -> Optional[Entity]:
        pass
