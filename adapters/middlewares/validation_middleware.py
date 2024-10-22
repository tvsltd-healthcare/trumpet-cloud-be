import os
import json

from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware

from adapters.entity_adapters.entity_validation import EntityAdapter
from application_layer.abstractions.entity_interface import IEntityGenerator


FILE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# CONFIG_FILE_PATH = os.path.join(FILE_PATH, 'config.json')
CONFIG_FILE_PATH = os.path.join(FILE_PATH, 'temp_config.json')


class ValidationMiddleware(BaseHTTPMiddleware):
    """
    Middleware for validating incoming requests.
    This middleware intercepts the request before it reaches the request handler.
    """

    async def dispatch(self, request: Request, call_next):
        with open(CONFIG_FILE_PATH) as config_file:
            configs = json.load(config_file)

        if request.method == 'POST':
            try:
                body = await request.json()
            except Exception:
                raise HTTPException(status_code=422, detail="Invalid JSON format")

                # for main_key, methods in ROUTES.items():
                #     if 'post' in methods and methods['post'] == request.url.path:
                #         entity_model = main_key
                #         if not entity_resources.get(entity_model):
                #             raise HTTPException(status_code=422,
                #                                 detail="Invalid entity type")
                #         model_entity = entity_resources[entity_model]
                #         is_valid = EntityAdapter().validate(entity_name=model_entity, data=body)
                #         if is_valid is not True:
                #             return JSONResponse(is_valid)
                #         return JSONResponse({"messages": "Valid"})
            for model in configs[0].get('models', []):
                for routes in model.get('routes', []):
                    if str.lower(routes.get('method')) == 'post' and str.lower(routes.get('url')) == request.url.path:
                        model_name = model

        # Continue processing if validation passes
        response = await call_next(request)
        return response
