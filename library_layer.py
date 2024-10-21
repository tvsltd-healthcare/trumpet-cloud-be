from typing import Any

from starlette.responses import JSONResponse
from wrap_restify import Libraries, Server
from adapters.lib_archi.controller import Controller
from application_layer.entities import get_resource_types
from lib_archi.base_application_service import BaseApplicationService
from lib_archi.base_repository import BaseRepository
from adapters.entity_generation.entity_adapter import EntityAdapter


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
    # "organizations": {
    #     "post": "/api/organizations",
    #     "get": "/api/organizations/{id}",
    #     "gets": "/api/organizations",
    # }
}

entity_resources = get_resource_types()

### Custom Middleware
import json
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for validating incoming requests.
    This middleware intercepts the request before it reaches the request handler.
    """

    async def dispatch(self, request: Request, call_next):
        # Optionally validate JSON payload
        if request.method == 'POST':
            try:
                body = await request.json()
                for main_key, methods in ROUTES.items():
                    if 'post' in methods and methods['post'] == request.url.path:
                        entity_model = main_key
                        if not entity_resources.get(entity_model):
                            raise HTTPException(status_code=422,
                                                detail="Invalid entity type")
                        model_entity = entity_resources[entity_model]
                        is_valid = EntityAdapter().validate(entity_name=model_entity, data=body)
                        if is_valid is not True:
                            return JSONResponse(is_valid)
                        return JSONResponse({"messages": "Valid"})

            except Exception:
                raise HTTPException(status_code=400, detail="Invalid JSON format")

        # Continue processing if validation passes
        response = await call_next(request)
        return response


def build_app_layer(server: Server) -> Any:
    for resource, routes in ROUTES.items():
        router_obj = server.router()
        klass = entity_resources[resource]

        repo = BaseRepository[klass]()
        app_service = BaseApplicationService[klass](repo)
        controller = Controller[klass](app_service)

        for verb, _endpoint in routes.items():
            if verb == "post":
                controller.post.__annotations__["entity"] = klass
                router_obj.post(url=_endpoint, endpoint=controller.post)
            elif verb == "get":
                router_obj.get(url=_endpoint, endpoint=controller.get)
            elif verb == "gets":
                router_obj.get(url=_endpoint, endpoint=controller.get_collection)

        server.use(router_obj)


def launch_app_layer():
    server = Server(Libraries.FASTAPI())

    _ = build_app_layer(server)

    server.use(RequestValidationMiddleware)
    server.listen(port=8080)


if __name__ == '__main__':
    launch_app_layer()
