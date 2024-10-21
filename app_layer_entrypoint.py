import functools
import os
import json

from typing import Dict
from functools import partial

from starlette.responses import JSONResponse
from wrap_restify import Libraries, Server
from wrap_restify.abstractions.routers import IRouter

from application_layer.entities import get_resource_types
from lib_archi.base_application_service import BaseApplicationService
from lib_archi.base_controller import BaseController
from adapters.lib_archi_adoption.inmemory_repository import InMemoryRepository
from adapters.entity_generation.entity_adapter import EntityAdapter

from dotenv import load_dotenv

from lib_archi.base_repository import BaseRepository

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
# CONFIG_FILE_PATH = os.path.join(FILE_PATH, 'config.json')
CONFIG_FILE_PATH = os.path.join(FILE_PATH, 'temp_config.json')

load_dotenv()


def get_verbs_mapping(controller, router_obj) -> Dict:
    """
    Returns a dictionary that maps HTTP verbs to their corresponding controller and router methods.
    """
    return {
        "get": (controller.get, router_obj.get),
        "get_collection": (controller.get_collection, router_obj.get),
        "post": (controller.post, router_obj.post),
        "put": (controller.put, router_obj.put),
        "patch": (controller.patch, router_obj.patch),
        "delete": (controller.delete, router_obj.delete)
    }







entity_resources = get_resource_types()




# import json
# from fastapi import Request, HTTPException
# from starlette.middleware.base import BaseHTTPMiddleware
#
#
# class RequestValidationMiddleware(BaseHTTPMiddleware):
#     """
#     Middleware for validating incoming requests.
#     This middleware intercepts the request before it reaches the request handler.
#     """
#
#     async def dispatch(self, request: Request, call_next):
#         # Optionally validate JSON payload
#         if request.method == 'POST':
#             try:
#                 body = await request.json()
#                 for main_key, methods in ROUTES.items():
#                     if 'post' in methods and methods['post'] == request.url.path:
#                         entity_model = main_key
#                         if not entity_resources.get(entity_model):
#                             raise HTTPException(status_code=422,
#                                                 detail="Invalid entity type")
#                         model_entity = entity_resources[entity_model]
#                         is_valid = EntityAdapter().validate(entity_name=model_entity, data=body)
#                         if is_valid is not True:
#                             return JSONResponse(is_valid)
#                         return JSONResponse({"messages": "Valid"})
#
#             except Exception:
#                 raise HTTPException(status_code=400, detail="Invalid JSON format")
#
#         # Continue processing if validation passes
#         response = await call_next(request)
#         return response


def build_app_layer(repository: BaseRepository, server: Server) -> IRouter:
    """Builds the application layer by registering routes and controllers.

    This function reads the application's configuration from a JSON file and sets
    up the server's routers and controllers based on the defined models and routes.
    For each model, it creates a repository, service, and controller, and registers
    the routes with the corresponding HTTP methods (e.g., POST).

    Args:
        server (Server): The server instance where routers and controllers
            are to be registered.
        repository (BaseRepository): The repository to register the routes and controllers

    Returns:
        Any: The result of building the app layer, though typically the
        return IRouter in the process.

    Raises:
        FileNotFoundError: If the configuration file specified by `CONFIG_FILE_PATH`
            is not found.
        json.JSONDecodeError: If the configuration file contains invalid JSON.
        KeyError: If expected keys (like 'name' or 'routes') are missing from the
            model definitions in the configuration.
    """
    # get all the routers of the application
    with open(CONFIG_FILE_PATH) as config_file:
        configs = json.load(config_file)

    for model in configs[0].get('models', []):
        router_obj = server.router()
        entity_stub_obj = entity_resources.get(model.get('name', None), None)

        # repo = InMemoryRepository[entity_stub_obj]()
        repo = repository[entity_stub_obj]()
        app_service = BaseApplicationService[entity_stub_obj](repo)
        controller = BaseController[entity_stub_obj](app_service)

        for routes in model.get('routes', []):
            verbs_mapping = get_verbs_mapping(controller, router_obj)
            route_method = str.lower(routes['method'])

            if route_method in verbs_mapping:
                method_controller, method_router = verbs_mapping[route_method]
                if route_method == "post" or route_method == "put" or route_method == "patch":
                    method_controller.__annotations__["entity"] = entity_stub_obj
                method_router(url=routes.get('url', ""), endpoint=method_controller)

        server.use(router_obj)

        return router_obj


def launch_app_layer():
    """Launches the application layer by creating and starting the server.

    This function initializes a FastAPI server, builds the application layer
    on top of the server, adds a request validation middleware, and listens on
    port 8080.

    The server is created using the `FASTAPI` library from `Libraries`,
    and the app layer is built using the `build_app_layer` function.
    The `RequestValidationMiddleware` is applied to ensure request data validation
    before listening for requests on port 8080.

    Raises:
        Any exception that occurs during server startup or middleware usage.
    """
    server = Server(Libraries.FASTAPI())

    _ = build_app_layer(repository=InMemoryRepository, server=server)
    # server.use(RequestValidationMiddleware)

    server.listen(port=os.getenv("PORT", 8080))
