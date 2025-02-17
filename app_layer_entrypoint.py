import os
import json

from logic_loader import load_logics
from wrap_restify import Libraries, Server
from wrap_restify.abstractions.routers import IRouter
from adapters.response_adapters import ResponseHandler
from application_layer.entities import get_resource_types
from lib_archi.base_application_service import BaseApplicationService
from lib_archi.base_controller import BaseController
from adapters.lib_archirs.orm_repository import OrmRepository
from adapters.lib_archirs.fastapi_controller import FastapiController
from lib_archi.base_repository import BaseRepository
from adapters.middlewares.validation_middleware import ValidationMiddleware
from adapters.middlewares.cors import CorsConfig
from adapters.wrap_orm_adapters.orm_adapter import OrmAdapter
from application_layer.abstractions.orm_interface import IOrm
from application_layer.abstractions.controller_interface import IController
from adapters.middlewares.response_middleware import ResponseMiddleware

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = os.path.join(FILE_PATH, 'config.json')

load_dotenv()
entity_resources = get_resource_types()
logic_map = load_logics()

def _generate_orm_wrapper():
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    # Create a SQLAlchemy engine
    engine = create_engine(f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database}')

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    orm: IOrm = OrmAdapter(session)

    return orm


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
        KeyError: If expected keys (like 'name' or 'routes') are missing from the=
            model definitions in the configuration.
    """
    # get all the routers of the application
    with open(CONFIG_FILE_PATH) as config_file:
        configs = json.load(config_file)

    orm = _generate_orm_wrapper()

    for model in (configs[0].get('models', [])):
        router_obj = server.router()
        entity_stub_obj = entity_resources.get(model.get('name'))

        if not entity_stub_obj:
            continue
        response_handler = ResponseHandler()

        if not entity_stub_obj:
            continue

        repo = repository[entity_stub_obj](orm)
        print('logic_map.get=model.get', logic_map.get(model.get('name')))
        app_service = BaseApplicationService[entity_stub_obj](repo, logic_map.get(model.get('name'), {}))
        base_controller = BaseController[entity_stub_obj](app_service, response_handler)
        controller: IController = FastapiController(base_controller)

        for routes in model.get('routes', []):
            route_method = str.lower(routes['method'])

            if str.lower(route_method) == "post":
                controller.post.__annotations__["entity"] = entity_stub_obj
                router_obj.post(url=routes.get('url', ""), endpoint=controller.post)
            elif str.lower(route_method) == "get":
                router_obj.get(url=routes.get('url', ""), endpoint=controller.get)
            elif str.lower(route_method) == "get_collection":
                router_obj.get(url=routes.get('url', ""), endpoint=controller.get_collection)
            elif str.lower(route_method) == "put":
                controller.put.__annotations__["entity"] = entity_stub_obj
                router_obj.put(url=routes.get('url', ""), endpoint=controller.put)
            elif str.lower(route_method) == "patch":
                controller.patch.__annotations__["entity"] = entity_stub_obj
                router_obj.patch(url=routes.get('url', ""), endpoint=controller.patch)
            elif str.lower(route_method) == "delete":
                controller.delete.__annotations__["entity"] = entity_stub_obj
                router_obj.delete(url=routes.get('url', ""), endpoint=controller.delete)
            else:
                raise NotImplementedError("This method is not supported in the base class.")

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

    # # Configure and apply CORS
    cors_config = CorsConfig(origins=os.getenv('ALLOWED_HOSTS', '*').split(','))

    _ = build_app_layer(repository=OrmRepository, server=server)

    server.use(ValidationMiddleware)
    server.use(ResponseMiddleware)
    cors_config.apply_to_server(server=server)

    server.listen(port=os.getenv("PORT", 8000), host=os.getenv("HOST", "127.0.0.1"))
