from typing import Dict

from application_layer.abstractions.entity_interface import IEntityGenerator
from wrap_validate import EntryPoint

class EntityAdapter(IEntityGenerator):
    def __init__(self):
        self.entity = EntryPoint()

    def create(self, entity_name: str, input_dict: Dict):
        return self.entity.loader.load_schema(name=entity_name, schema=input_dict)

    def validate(self, entity_name: str, data: Dict):
        return self.entity.validator.validate(schema=entity_name, data=data)
