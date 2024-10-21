from typing import Any, Dict

from .product import Product
from .user import Users
from .organizations import Organizations

from adapters.entity_generation.entity_adapter import EntityAdapter


entity_adapter_obj = EntityAdapter()


def get_resource_types() -> Dict[str, Any]:
    _user = entity_adapter_obj.create(entity_name='Users', input_dict=Users)
    _organizations = entity_adapter_obj.create(entity_name='Organizations', input_dict=Organizations)

    return {"Users": _user, "Organizations": _organizations}
