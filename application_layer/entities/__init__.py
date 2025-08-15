import os
import importlib

from typing import Any, Dict, Tuple

from adapters.entity_adapters.entity_validation import EntityAdapter


entity_adapter_obj = EntityAdapter()
current_dir = os.path.dirname(__file__)


def get_resource_types() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Loads and processes entity definitions from Python modules in the current directory.

    This function dynamically imports Python modules in the current directory (excluding `__init__.py`)
    and extracts any dictionaries from those modules. Each dictionary is assumed to represent an entity
    definition, and an adapter is used to create resource objects from these definitions.

    Returns:
        Dict[str, Any]: A dictionary where the keys are the names of the entities and the values
        are resource objects created using the entity adapter.
    """
    resource_types = {}
    patch_entity_resources = {}

    for filename in os.listdir(current_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]
            module = importlib.import_module(f'.{module_name}', package=__name__)

            for attr_name in dir(module):
                # Skip special and built-in attributes (starting with __)
                if not attr_name.startswith('__'):
                    attr_value = getattr(module, attr_name)
                    if isinstance(attr_value, dict):  # If it's a dictionary, it's an entity definition
                        # Dynamically create the resource and add it to the resource_types dictionary

                        resource_types[attr_name] = entity_adapter_obj.create(entity_name=attr_name, input_dict=attr_value)

                        patch_entity_resources[attr_name] = entity_adapter_obj.create(entity_name=attr_name,
                                                                                      input_dict= make_all_the_fields_optional(attr_value))

    return resource_types, patch_entity_resources

def make_all_the_fields_optional(attr_value):
    attr_value_all_fields_optional = {}
    for column, properties in attr_value.items():
        attr_value_all_fields_optional[column] = {k: v for k, v in properties.items() if k != 'required'}

    return attr_value_all_fields_optional