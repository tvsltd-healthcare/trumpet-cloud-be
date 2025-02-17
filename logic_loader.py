import importlib
import os
import glob

LOGIC_FOLDER = "domain_layer.logics"

def load_logics():
    logic_map = {}

    # Scan for all Python files in the logic folder (except __init__.py)
    logic_files = glob.glob(os.path.join(LOGIC_FOLDER.replace(".", "/"), "*.py"))
    print('logic_files',logic_files)

    for file in logic_files:
        module_name = os.path.basename(file)[:-3]  # Remove `.py`
        if module_name == "__init__":
            continue  # Skip init file

        # Import module dynamically
        module_path = f"{LOGIC_FOLDER}.{module_name}"
        module = importlib.import_module(module_path)

        # Extract the resource name from the filename (e.g., `users_logic.py` → `users`)
        resource_name = module_name.replace("_logic", "").capitalize()
        print('resource_name', resource_name)

        # Store logic methods in a nested dictionary
        logic_map[resource_name] = {
            "get": getattr(module, "get_logic", None),
            "post": getattr(module, "post_logic", None),
            "put": getattr(module, "put_logic", None),
            "delete": getattr(module, "delete_logic", None),
        }

    return logic_map
