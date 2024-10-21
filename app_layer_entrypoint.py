from typing import Any

from wrap_restify import Libraries, Server
from adapters.lib_archi.controller import Controller
from application_layer.entities import get_resource_types
from lib_archi.base_application_service import BaseApplicationService
from lib_archi.base_repository import BaseRepository
from adapters.entity_generation.entity_adapter import EntityAdapter
from wrap_validate import EntryPoint


ROUTES = {
    # "products": {
    #     "post": "/api/products",
    #     "get": "/api/product/{id}",
    #     "gets": "/api/products",
    # },
    "users": {
        "post": "/api/users",
        "get": "/api/users/{id}",
        "gets": "/api/users",
    },
    "organizations": {
        "post": "/api/organizations",
        "get": "/api/organizations/{id}",
        "gets": "/api/organizations",
    }
}

def validate_custom(data: dict):
    # Implement your custom validation logic here
    if not data.get("name"):
        raise ValueError("required_field is missing")
    return data



def build_app_layer(server: Server) -> Any:
    # entity names and api endpoints required for them (cli input)
    entity_resources = get_resource_types()
    entity_adapter_obj = EntityAdapter(EntryPoint())

    for resource, routes in ROUTES.items():
        # Create a new router for each resource to ensure unique memory location
        router_obj = server.router()

        klass = entity_adapter_obj.create(entity_name=resource, input_dict=entity_resources[resource])

        repo = BaseRepository[klass]()
        app_service = BaseApplicationService[klass](repo)
        controller = Controller[klass](app_service)

        for verb, _endpoint in routes.items():
            if verb == "post":
                controller.post.__annotations__["entity"] = klass
                router_obj.post(url=_endpoint, endpoint=controller.post)

            elif verb == "get":
                router_obj.get(url=_endpoint, endpoint=controller.get)
            elif verb == "gets":  # here is the conditionals
                router_obj.get(url=_endpoint, endpoint=controller.get_collection)

        server.use(router_obj)


def launch_app_layer():
    server = Server(Libraries.FASTAPI())
    _ = build_app_layer(server)
    server.listen(port=8080)
