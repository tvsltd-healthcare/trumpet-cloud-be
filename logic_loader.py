import importlib.util
import os
import glob
from typing import Dict, Any

LOGIC_FOLDER = "domain_layer/logics"

def load_logics() -> Dict[str, Dict[str, Any]]:
    """
    Dynamically loads logic files following the pattern <api_verb>_<model_name>_logic.py.

    Returns:
        Dict[str, Dict[str, Any]]: A nested dictionary with model names as keys and
        their corresponding API verb logic as values.
    """
    logic_map = {}

    # ✅ Use absolute path
    abs_logic_folder = os.path.abspath(LOGIC_FOLDER)
    logic_files = glob.glob(os.path.join(abs_logic_folder, '*_logic.py'))

    for file_path in logic_files:
        file_name = os.path.basename(file_path)
        if '__init__.py' in file_name:
            continue  # Skip __init__.py

        # Extract verb and model from filename (e.g., get_users_logic.py)
        parts = file_name.replace('_logic.py', '').split('_')
        if len(parts) < 2:
            continue

        api_verb, model_name = parts[0], '_'.join(parts[1:])

        # Dynamically import the module
        spec = importlib.util.spec_from_file_location(f"{api_verb}_{model_name}_logic", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Ensure the module has an 'execute' method
        logic_function = getattr(module, "execute", None)
        if logic_function:
            model_key = model_name.capitalize()
            if model_key not in logic_map:
                logic_map[model_key] = {}
            logic_map[model_key][api_verb] = logic_function
        else:
            pass

    return logic_map
