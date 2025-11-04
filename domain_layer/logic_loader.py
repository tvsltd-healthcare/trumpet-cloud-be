import os
import glob
import importlib.util
from typing import Dict, Any

SUPPORTED_VERBS = {"get", "post", "put", "patch", "delete", "get_collection"}
NON_RESOURCES_KEY = "non_resources"


def get_logic_files(path: str) -> list:
    """Returns a list of logic files from the given path."""
    return glob.glob(os.path.join(path, '*_logic.py'))


def extract_api_verb_and_model(file_name: str) -> tuple:
    """Extracts API verb and model name from the file name."""
    parts = file_name.replace('_logic.py', '').split('_')
    if len(parts) < 2:
        return None, None
    
    if '_'.join(parts[:2]) in SUPPORTED_VERBS:
        return '_'.join(parts[:2]), '_'.join(parts[2:])
    
    return parts[0], '_'.join(parts[1:])


def import_logic_module(file_path: str, module_name: str):
    """Dynamically imports a logic module and returns the execute function if available."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "execute", None) if hasattr(module, "execute") and callable(getattr(module, "execute")) else None


def load_logic_from_path(path: str, logic_map: Dict[str, Dict[str, Any]]):
    """Loads logic modules from a specified path and populates the logic_map."""
    logic_files = get_logic_files(path)

    for file_path in logic_files:
        file_name = os.path.basename(file_path)
        
        if '__init__.py' in file_name:
            continue
        
        api_verb, model_name = extract_api_verb_and_model(file_name)

        if not api_verb or api_verb not in SUPPORTED_VERBS:
            continue

        module_name = f"{api_verb}_{model_name}_logic"
        
        logic_function = import_logic_module(file_path, module_name)
        
        if not logic_function:
            continue
        
        model_key = model_name.capitalize()
        if model_key not in logic_map:
            logic_map[model_key] = {}
        
        logic_map[model_key][api_verb] = logic_function

def load_logic_from_non_resource_path(path: str, logic_map: Dict[str, Dict[str, Any]]):
    """Loads non resource logic modules from a specified path and populates the logic_map."""
    logic_files = get_logic_files(path)

    for file_path in logic_files:
        file_name = os.path.basename(file_path)

        if '__init__.py' in file_name:
            continue

        module_name = file_name.removesuffix("_logic.py")

        logic_function = import_logic_module(file_path, module_name)
        
        if not logic_function:
            continue

        if NON_RESOURCES_KEY not in logic_map:
            logic_map[NON_RESOURCES_KEY] = {}

        logic_map[NON_RESOURCES_KEY][module_name] = logic_function


def load_logics(path: str) -> Dict[str, Dict[str, Any]]:
    """
    Dynamically loads logic files following the pattern <api_verb>_<model_name>_logic.py.
    
    Supported API verbs: get, post, put, patch, delete, get_collection.
    
    Returns:
        Dict[str, Dict[str, Any]]: A nested dictionary with model names as keys and
        their corresponding API verb logic as values.
    """
    logic_map = {}
    load_logic_from_path(path, logic_map)
    load_logic_from_non_resource_path(os.path.join(path, NON_RESOURCES_KEY), logic_map)
    return logic_map
