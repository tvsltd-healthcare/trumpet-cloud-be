import importlib.util
import os
import glob
from typing import Dict, Any

LOGIC_FOLDER = os.getenv("LOGIC_PATH")

def load_logics() -> Dict[str, Dict[str, Any]]:
    """
    Dynamically loads logic files following the pattern <api_verb>_<model_name>_logic.py.

    Supported API verbs: get, post, put, patch, delete, get_collection.

    Returns:
        Dict[str, Dict[str, Any]]: A nested dictionary with model names as keys and
        their corresponding API verb logic as values.
    """
    logic_map = {}

    # Use absolute path to locate logic folder
    abs_logic_folder = os.path.abspath(LOGIC_FOLDER)
    logic_files = glob.glob(os.path.join(abs_logic_folder, '*_logic.py'))

    # Supported API verbs
    supported_verbs = {"get", "post", "put", "patch", "delete", "get_collection"}

    for file_path in logic_files:
        file_name = os.path.basename(file_path)
        if '__init__.py' in file_name:
            continue

        # Extract verb and model from filename (e.g., get_users_logic.py OR get_collection_users_logic.py)
        parts = file_name.replace('_logic.py', '').split('_')

        # Handle cases where the verb is two words like "get_collection"
        if len(parts) < 2:
            continue

        # Check for verbs with two words (like "get_collection")
        if '_'.join(parts[:2]) in supported_verbs:
            api_verb = '_'.join(parts[:2])  # e.g., "get_collection"
            model_name = '_'.join(parts[2:])  # e.g., "users"
        else:
            api_verb = parts[0]  # e.g., "get"
            model_name = '_'.join(parts[1:])  # e.g., "users"

        # Validate API verb
        if api_verb not in supported_verbs:
            continue  # Skip if the verb is not recognized

        # Dynamically import the module
        spec = importlib.util.spec_from_file_location(f"{api_verb}_{model_name}_logic", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Ensure the module has an 'execute' function
        logic_function = getattr(module, "execute", None)
        if logic_function and callable(logic_function):
            model_key = model_name.capitalize()
            if model_key not in logic_map:
                logic_map[model_key] = {}
            logic_map[model_key][api_verb] = logic_function
        else:
            pass

    return logic_map
