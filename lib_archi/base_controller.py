from typing import TypeVar, Generic, Optional, Any
from .base_application_service import BaseApplicationService

Entity = TypeVar('Entity')


class BaseController(Generic[Entity]):
    def __init__(self, appService: BaseApplicationService[Entity]):
        self.appService: BaseApplicationService[Entity] = appService

    def post(self, entity: Entity):
        return self.appService.post(entity.id, entity)

    def get(self, id: str) -> Optional[Entity]:
        return self.appService.get(id)
