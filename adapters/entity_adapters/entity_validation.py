from typing import Dict

from application_layer.abstractions.entity_interface import IEntityGenerator
from wrap_validate import load_schema, validate_schema


class EntityAdapter(IEntityGenerator):
    """Adapter class for creating and validating entities.

    This class provides methods for loading entity schemas and validating data against them.
    It implements the IEntityGenerator interface.
    """
    def create(self, entity_name: str, input_dict: Dict):
        """Creates an entity using the provided schema.

        Args:
            entity_name (str): The name of the entity to be created.
            input_dict (Dict): A dictionary containing the schema for the entity.

        Returns:
            Any: The result of loading the schema using the provided entity name and schema.
        """
        return load_schema(name=entity_name, schema=input_dict)

    def validate(self, entity_name: str, data: Dict):
        """Validates the data against the specified entity schema.

        Args:
            entity_name (str): The name of the entity schema to validate against.
            data (Dict): A dictionary containing the data to be validated.

        Returns:
            Any: The result of validating the data against the entity schema.
        """
        return validate_schema(schema=entity_name, data=data)
