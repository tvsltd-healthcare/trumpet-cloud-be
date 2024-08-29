from typing import Any, Dict
from wrap_restify import Frameworks, Server
from adapters.lib_archi.controller import Controller
from application_layer.abstractions.applicaiton_interface.icontroller import IController
from application_layer.entities import get_resource_types
from lib_archi.base_application_service import BaseApplicationService
from lib_archi.base_repository import BaseRepository

# Entity


# Repository

# 1. Implementing lib-irc Communication interface
#    polymorphic => REST, gRPC, socket, message broker


# ApplicationService

# 1. ✅ Using Repositories (one or more) to create update resources
# 2. → Invoking lib-logic registered domain services
#      to manipulate data (run business requirements)


# Controller


# Routes

_routes: Dict[str, Dict[str, str]] = {
    "products": {
        "post": "/api/products",
        "get": "/api/products/{id}",
    },
    # "users": {
    #     "post": "/api/users",
    #     "get": "/api/users/{id}",
    # }
}


def hello():
    """_summary_

    Returns:
        _type_: _description_
    """
    return "Hello"


def build_application_layer(server: Server) -> Any:
    """_summary_

    Args:
        server (Server): _description_

    Returns:
        Any: _description_
    """
    # One router for all resources and their APIs
    router = server.router()

    # entity names and api endpoints required for them (cli input)
    entity_resources: Dict[str, Any] = get_resource_types()

    for resource, routes in _routes.items():
        klass = entity_resources[resource]

        repo: BaseRepository[klass] = BaseRepository[klass]()
        app_service: BaseApplicationService[klass] = BaseApplicationService[klass](
            repo)
        controller: IController = Controller[klass](app_service)

        for verb, _endpoint in routes.items():
            if (verb == "post"):
                # TODO: fix in instance level. seems working in class/static level
                # setattr(controller.post.__annotations__, 'entity', klass)
                # controller.post.__annotations__.update({'entity': klass})
                controller.post.__annotations__["entity"] = klass
                router.post(url=_endpoint, endpoint=controller.post)
            elif (verb == "get"):
                router.get(url=_endpoint, endpoint=controller.get)

    return router


def launch_application_layer():
    """_summary_
    """
    server = Server(Frameworks.FASTAPI())

    router = build_application_layer(server)
    server.use(router)

    server.listen(port=8080)
