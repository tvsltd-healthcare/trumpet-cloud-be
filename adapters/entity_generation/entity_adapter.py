from typing import Dict

from application_layer.abstractions.entity_interface import IEntityGenerator


class EntityAdapter(IEntityGenerator):
    def __init__(self, entity_adapter):
        self.entity = entity_adapter

    def create(self, entity_name: str, input_dict: Dict):
        return self.entity.loader.load_schema(name=entity_name, schema=input_dict)
