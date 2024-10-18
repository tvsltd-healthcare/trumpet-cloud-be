from .product import Product
from .user import User
from .organizations import Organizations

from typing import Any, Dict


def get_resource_types() -> Dict[str, Any]:
    return {"products": Product, "users": User, "organizations": Organizations}
