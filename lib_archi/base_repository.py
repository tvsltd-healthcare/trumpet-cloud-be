from typing import TypeVar, Generic, Optional, List, Dict

Entity = TypeVar('Entity')


class BaseRepository(Generic[Entity]):
    def __init__(self):
        self.entities: Dict[str, Entity] = {}

    def get(self, id: str) -> Optional[Entity]:
        return self.entities.get(id)

    def get_collection(self) -> List[Entity]:
        return list(self.entities.values())

    def create(self, id: str, entity: Entity) -> None:
        if entity.id not in self.entities:
            self.entities[entity.id] = entity
        else:
            raise ValueError(f"Entity with id {entity.id} already exists")

    def update(self, id: str, entity: Entity) -> None:
        if id in self.entities:
            self.entities[id] = entity
        else:
            raise ValueError(f"Entity with id {id} does not exist")

    def delete(self, id: str) -> bool:
        if id in self.entities:
            del self.entities[id]
            return True
        return False
