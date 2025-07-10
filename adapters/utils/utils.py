import json
import re
import os
from http.client import HTTPException
from typing import Optional, Dict

FILE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CONFIG_FILE_PATH = os.path.join(FILE_PATH, 'config.json')


def get_model_name(path: str, method_name: str, configs: dict) -> Optional[str]:
    """
    Get the model name based on the request and configuration.

    Args:
        method_name: request method name.
        path: request path.
        configs (dict): Configuration data.

    Returns:
        Optional[str]: The model name if found, otherwise None.
    """
    for model in configs[0].get('models', []):
        for route in model.get('routes', []):
            route_name_lower = route.get('method', '').lower()

            if route_name_lower == "get_collection":
                route_name_lower = "get"

            if route_name_lower == method_name.lower() and is_route_and_request_same(route, path):
                return model.get('name')
    return None


def is_route_and_request_same(route: Dict, path: str) -> bool:
    """
    Check if the route and request path match.

    Args:
        path: request path.
        route (Dict): Route configuration.

    Returns:
        bool: True if the paths match, False otherwise.
    """
    route_path = normalize_path(route.get('url', '').lower())
    current_request_path = normalize_path(path.lower())
    return route_path == current_request_path


def normalize_path(path: str) -> str:
    """
    Normalize a path by replacing numeric IDs or placeholders with a generic placeholder.

    Args:
        path (str): The path to normalize.

    Returns:
        str: The normalized path.
    """
    path = re.sub(r"\d+", "{id}", path)
    path = re.sub(r"\{.*?\}", "{id}", path)
    return path


def load_config() -> dict:
    """
    Load the configuration file.

    Returns:
        dict: Parsed configuration data.

    Raises:
        HTTPException: If the config file is missing or invalid.
    """
    try:
        with open(CONFIG_FILE_PATH, 'r') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Config file not found.")
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="Config file is invalid.")
