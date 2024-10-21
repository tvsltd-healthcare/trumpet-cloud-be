from .base_repository import BaseRepository
from typing import TypeVar, Generic, Optional, List

Entity = TypeVar('Entity')


class BaseApplicationService(Generic[Entity]):
    def __init__(self, repository: BaseRepository[Entity]):
        self.repository: BaseRepository[Entity] = repository

    def get(self, id: str) -> Optional[Entity]:
        # if (Logics.get('get', 'Entity')):
        #    logic: Logic = Logics.get('get', 'Entity')
        #    logic(self, id)
        # else
        return self.repository.get(id)

    def get_collection(self) -> List[Entity]:
        return self.repository.get_collection()

    def post(self, entity: Entity) -> None:
        self.repository.post(entity)

    def put(self, entity: Entity) -> None:
        self.repository.update(entity)

    def patch(self, entity: Entity) -> None:
        self.repository.update(entity)

    def delete(self, id: str) -> bool:
        self.repository.delete(id)
