import json
import os
import re

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from wrap_restify import Libraries, Server
from wrap_restify.abstractions.routers import IRouter

from adapters.auth_adapters.auth_handler_factory import AuthHandlerFactory
from adapters.email_service_adapters.email_service_handler_factory import EmailServiceHandlerFactory, EmailServiceType
from adapters.fga_authorization_adapters import Mechanism as FGA_authorization_mechanism, FgaAuthorizationFactory
from adapters.fga_authorization_adapters.openfga_authorization_adapter import Configuration as OpenFgaConfiguration
from adapters.lib_archirs.non_resource_controller_adapter import NonResourceControllerAdapter
from adapters.lib_archirs.orm_repository import OrmRepository
from adapters.lib_repo_discovery.repo_direct_invoker_adapter import RepoDirectInvokerAdapter
from adapters.lib_repo_discovery.repo_discovery_getter_adapter import RepoDiscoveryGetterAdapter
from adapters.lib_repo_discovery.repo_discovery_setter_adapter import RepoDiscoverySetterAdapter
from adapters.middlewares.auth_middleware import AuthMiddleware
from adapters.middlewares.authorization_middleware import AuthorizationMiddleware
from adapters.middlewares.cors import CorsConfig
from adapters.middlewares.pagination_middleware import pagination_middleware
from adapters.middlewares.rate_limit_middleware import rate_limit_middleware_factory
from adapters.middlewares.response_middleware import ResponseMiddleware
from adapters.middlewares.validation_middleware import ValidationMiddleware
from adapters.password_adapters.bcrypt_adapters import PasswordHandler
from adapters.response_adapters import ResponseHandler
from adapters.wrap_orm_adapters.orm_adapter import OrmAdapter
from application_layer.abstractions.app_repo_discovery_setter_interface import IAppRepoDiscoverySetter
from application_layer.abstractions.controller_interface import IController
from application_layer.abstractions.non_resource_controller_interface import INonResourceController
from application_layer.abstractions.orm_interface import IOrm
from application_layer.entities import get_resource_types
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.password_manager_interface import IPasswordHandler
from domain_layer.auth_manager import AuthManager
from domain_layer.dependency.email_service_manager import EmailServiceManager
from domain_layer.logic_loader import load_logics
from domain_layer.password_manager import PasswordManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from lib_archi.abstractions.non_resource_app_service_interface import ILibNonResourceService
from lib_archi.abstractions.non_resource_controller_interface import ILibNonResourceController
from lib_archi.base_application_service import BaseApplicationService
from lib_archi.base_controller import BaseController
from adapters.lib_archirs.orm_repository import OrmRepository
from lib_archi.base_repository import BaseRepository
from lib_archi.non_resource_app_service import NonResourceAppService
from lib_archi.non_resource_controller import NonResourceController
from lib_archi.repository_gateway_service import RepositoryGatewayService
from lib_repo_discovery.repo_discovery import RepoDiscovery

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE_PATH = os.path.join(FILE_PATH, 'config.json')

entity_resources = get_resource_types()
logic_folder_path = os.getenv("LOGIC_PATH")
logic_map = load_logics(logic_folder_path)

# JWT and authentication configuration
auth_config = {"type": "JWT",  # Authentication type, can be "JWT" or others in the future
    "jwt": {"secret": os.getenv("JWT_SECRET"),  # Secret for JWT
        "algorithm": os.getenv("JWT_ALGORITHM"),  # JWT algorithm
        "expiry": int(os.getenv("JWT_EXPIRY")),  # Expiry time for JWT
    }}

auth_handler = AuthHandlerFactory.get_handler(auth_config)
AuthManager.set(auth_handler)
auth_middleware = AuthMiddleware(auth_handler)

open_fga_configuration: OpenFgaConfiguration = {"OPENFGA_API_URL": os.getenv("OPENFGA_API_URL"),
    "OPENFGA_STORE_ID": os.getenv("OPENFGA_STORE_ID"), "OPENFGA_MODEL_ID": os.getenv("OPENFGA_MODEL_ID")}

authorization_handler = FgaAuthorizationFactory.create(FGA_authorization_mechanism.OPEN_FGA, open_fga_configuration)
authorization_middleware = AuthorizationMiddleware(authorizer=authorization_handler)

# SMTP email service configuration
email_service_configuration = {"name": EmailServiceType.SMTP,
    "config": {"host": os.getenv("EMAIL_HOST"), "port": int(os.getenv("EMAIL_PORT")),
        "username": os.getenv("EMAIL_USERNAME"), "password": os.getenv("EMAIL_PASSWORD"),
        "subject": os.getenv("EMAIL_SUBJECT"), "sender_email": os.getenv("SENDER_EMAIL")}}

# Initialize the AuthMiddleware with the configuration
repo_discovery: RepoDiscovery = RepoDiscovery()
repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryGetterAdapter(repo_discovery)
repo_discovery_setter_adapter: IAppRepoDiscoverySetter = RepoDiscoverySetterAdapter(repo_discovery)

RepoDiscoveryManager.set(repo_discovery_getter_adapter)

# Manager for Password
password_handler: IPasswordHandler = PasswordHandler()
PasswordManager.set(password_handler)

email_service_factory = EmailServiceHandlerFactory.get_handler(email_service_configuration)
EmailServiceManager.set(email_service_factory)


def convert_to_snake_case(name: str) -> str:
    # This converts to snake_case and keeps the first letter capitalized
    return name[0] + re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name[1:]).lower()


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
    response_handler = ResponseHandler()

    for model in (configs[0].get('models', [])):
        model_name = model.get('name')
        router_obj = server.router()
        entity_stub_obj = entity_resources.get(model_name)

        if not entity_stub_obj:
            continue

        if not entity_stub_obj:
            continue

        repo = repository[entity_stub_obj](orm)

        model_key = convert_to_snake_case(model_name)
        
        repo_gateway_service = RepositoryGatewayService[entity_stub_obj](repo, logic_map.get(model_key, {}))
        repo_invoker: IAppRepoInvoker = RepoDirectInvokerAdapter(repo_gateway_service)
        repo_discovery_setter_adapter.set_repo_invoker(model_name, repo_invoker)

        app_service = BaseApplicationService[entity_stub_obj](repo, logic_map.get(model_key, {}))
        base_controller = BaseController[entity_stub_obj](app_service, response_handler)
        controller: IController = base_controller

        for routes in model.get('routes', []):
            route_method = str.lower(routes['method'])

            if str.lower(route_method) == "post":
                controller.post.__annotations__["entity"] = entity_stub_obj
                if routes['auth']:
                    router_obj.post(url=routes.get('url', ""), endpoint=controller.post,
                                   entity_class=entity_stub_obj, dependencies=[auth_middleware])
                else:
                    router_obj.post(url=routes.get('url', ""), endpoint=controller.post, entity_class=entity_stub_obj)
            elif str.lower(route_method) == "get":
                if routes['auth']:
                    router_obj.get(url=routes.get('url', ""), endpoint=controller.get,
                                   dependencies=[auth_middleware])
                else:
                    router_obj.get(url=routes.get('url', ""), endpoint=controller.get)
            elif str.lower(route_method) == "get_collection":
                if routes['auth']:
                    router_obj.get(url=routes.get('url', ""), endpoint=controller.get_collection,
                                   dependencies=[auth_middleware])
                else:
                    router_obj.get(url=routes.get('url', ""), endpoint=controller.get_collection)
            elif str.lower(route_method) == "put":
                controller.put.__annotations__["entity"] = entity_stub_obj
                if routes['auth']:
                    router_obj.put(url=routes.get('url', ""), endpoint=controller.put,
                                  entity_class=entity_stub_obj, dependencies=[auth_middleware])
                else:
                    router_obj.put(url=routes.get('url', ""), endpoint=controller.put, entity_class=entity_stub_obj)
            elif str.lower(route_method) == "patch":
                controller.patch.__annotations__["entity"] = entity_stub_obj
                if routes['auth']:
                    router_obj.patch(url=routes.get('url', ""), endpoint=controller.patch, entity_class=entity_stub_obj,
                                     dependencies=[auth_middleware])
                else:
                    router_obj.patch(url=routes.get('url', ""), endpoint=controller.patch, entity_class=entity_stub_obj)
            elif str.lower(route_method) == "delete":
                controller.delete.__annotations__["entity"] = entity_stub_obj
                if routes['auth']:
                    router_obj.delete(url=routes.get('url', ""), endpoint=controller.delete,
                                      dependencies=[auth_middleware])
                else:
                    router_obj.delete(url=routes.get('url', ""), endpoint=controller.delete)
            else:
                raise NotImplementedError("This method is not supported in the base class.")

        server.use(router_obj)

    non_resource_app_service: ILibNonResourceService = NonResourceAppService(logic_map.get('non_resources', {}))
    non_resource_controller: ILibNonResourceController = NonResourceController(non_resource_app_service)
    non_resource_controller_adapter: INonResourceController = NonResourceControllerAdapter(non_resource_controller,
                                                                                           response_handler)

    router_obj = server.router()

    non_resource_config = configs[0].get('non_resources', {})
    for routes in (non_resource_config.get('routes', [])):
        route_verb = str.lower(routes['verb'])
        url = routes.get('url', "")

        if str.lower(route_verb) == "post":
            router_obj.post(url=url, endpoint=non_resource_controller_adapter.perform)
        elif str.lower(route_verb) == "get":
            router_obj.get(url=url, endpoint=non_resource_controller_adapter.perform)

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
    # Redirect to HTTPS
    # server.use(HTTPSRedirectMiddleware)
    server.use(ResponseMiddleware)
    per_page = int(os.getenv("PER_PAGE", 10))
    server.use(pagination_middleware(per_page=per_page))
    rate_limit = int(os.getenv("RATE_LIMIT_REQUEST_PER_WINDOW"))
    time_window = int(os.getenv("RATE_LIMIT_TIME_WINDOW_IN_SECOND"))
    algorithm = os.getenv("RATE_LIMIT_ALGORITHM")
    server.use(rate_limit_middleware_factory(algorithm=algorithm, rate_limit=rate_limit, time_window=time_window))
    cors_config.apply_to_server(server=server)

    server.listen(port=os.getenv("PORT", 8000), host=os.getenv("HOST", "127.0.0.1"))
