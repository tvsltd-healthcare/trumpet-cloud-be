import re

from fastapi import Request, HTTPException
from starlette import status

from adapters.middlewares.validation_middleware import ValidationMiddleware


class AuthorizationMiddleware:
    def __init__(self, authorizer):
        self.authorizer = authorizer
        self.configs = ValidationMiddleware._load_config()

    def __call__(self, request: Request):
        print("AuthorizationMiddleware called")

        user_id = request.state.user_id

        print(f"{user_id=}")

        relation = _get_relation(request=request)
        print(f"{relation=}")

        resource = _get_resource(request, configs=self.configs)
        print(f"{resource=}")

        authorization_response = self.authorizer.check(
            {
                "user_type": "user",
                "user_id": user_id,
                "resource_type": resource.get("type"),
                "resource_id": resource.get("id"),
                "action": relation
            }
        )

        print(f"{authorization_response=}")

        if not authorization_response.get("allowed"):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


def _get_user(request):
    user_id = request.headers["userid"]
    return {user_id}


def _get_resource(request, configs):
    resource_type = ValidationMiddleware._get_model_name(
        request=request, configs=configs
    )
    match = re.search(r"\d+$", str(request.url))
    resource_id = match.group(0)

    if request.method == 'POST':
        _get_parent(resource_type, )
    return {"type": resource_type, "id": resource_id}


def _get_relation(request: Request):
    http_method = request.method
    return http_method


def _get_parent(resource_type: str, configs: dict):
    print(resource_type)
    models = configs[0].get("models", []) or []

    model = _find_object(
        objects=models, key="name", value=resource_type
    )

    if not model.get("associations"):
        print("associations", model.get("associations"))
        return "system"

    return model.get()


def _find_object(objects, key, value):
    return next((obj for obj in objects if obj.get(key) == value), None)
