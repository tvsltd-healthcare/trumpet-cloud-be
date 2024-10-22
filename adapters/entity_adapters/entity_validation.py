from typing import Dict

from application_layer.abstractions.entity_interface import IEntityGenerator
from wrap_validate import load_schema, validate_schema


class EntityAdapter(IEntityGenerator):
    def create(self, entity_name: str, input_dict: Dict):
        return load_schema(name=entity_name, schema=input_dict)

    def validate(self, entity_name: str, data: Dict):
        return validate_schema(schema=entity_name, data=data)
