# 🧠 Logic Layer Guide

This directory contains **business logic handlers** for various endpoints in the application. Logic files are designed to be simple, composable units that operate using the abstracted `IRequest` interface and cleanly separate infrastructure concerns from business rules.

---

## 📁 Folder Structure

```text
logic/
├── get_users_logic.py
├── post_roles_logic.py
├── put_organizations_logic.py
├── delete_sessions_logic.py
├── non_resources/
│   ├── upload_file_logic.py
│   ├── health_check_logic.py
│   ├── send_email_verification_logic.py
```
---

## 📌 Naming Convention

- All **resource-based logic files** go directly inside the `logic/` folder.

  - **Format:** `{{verb_method}}_{{resource_name}}_logic.py`
  - **Examples:**
    - `get_users_logic.py`
    - `get_collection_users_logic.py`
    - `post_roles_logic.py`
    - `put_organizations_logic.py`

- All **non-resource logic files** (i.e., not tied to a RESTful resource) go inside the `logic/non_resources/` subfolder.

  - **Format:** `{{stripped_path}}_logic.py`, where:
    - Any slashes `/`, dashes `-`, or spaces are replaced with underscores `_`
  - **Examples:**
    - `/upload-file` → `upload_file_logic.py`
    - `/send/notification` → `send_notification_logic.py`
    - `/send-email-verification` → `send_email_verification_logic.py`


---

## 📌 Key Concepts

### ✅ `IRequest` (Abstract Request Object)

All logic functions receive a request wrapped in `IRequest`, which is:
- **Framework-agnostic**
- Decoupled from FastAPI or any other HTTP library
- Comes with helper methods like:
  - `get_json()`
  - `get_form_data()`
  - `get_files()`
  - `get_query_params()`
  - `get_path_params()`
  - `get_url()`
  - `get_path()`

> You don't interact with `fastapi.Request` directly. This makes testing and switching frameworks much easier.

---

### ✅ `@enforce_request_type()`

Every logic function must be decorated with `@enforce_request_type()` to ensure type safety and interface enforcement.

---

### ✅ Access other resouce repo with lib repo discovery

- Use `RepoDiscoveryManager.get()` to access your data layer:
- `repo_discovery_getter_adapter.get_repo_invoker("EntityName")` returns a **repo invoker**
- This invoker can:
  - `.get(query_dict)`
  - `.transact(method, payload, query_dict?)`
  - etc.

---

## 🧪 Writing a New Logic File for Resource Based Endpoints

Here’s a template to follow:

```python
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker

@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Handles the execution of business logic for a given endpoint.

    Args:
        request (IRequest): An abstracted request object that provides access to request data 
                            (e.g., JSON body, form data, files, query params) in a framework-agnostic way.
                            check domain_layer.abstractions.request_interface for all the methods
        repo: The endpoint's own repository instance used for data operations (CRUD, queries, etc.).
                check lib_archi/base_repository.py for all the methods
        entity (Optional[Any]): A Pydantic-validated object containing structured request data, 
                                typically parsed and validated by the framework before reaching this layer.

    Returns:
        Any: The result of the business logic execution, typically a dictionary or primitive that the caller
             serializes as an HTTP response.
    """

    # Access data
    form_data = request.get_form_data()
    json_data = request.get_json()
    path_params = request.get_path_params()

    # Use repository of own Repo
    org = repo.get({ "id": 5 })

    # Use repositories of other Repo
    repo_manager = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_manager.get_repo_invoker("Users")

    # Business logic
    user = user_repo.transact("POST", form_data)
    user = user_repo.transact("PUT", form_data, { "id": 1 })
    user = user_repo.transact("DELETE", {}, { "id": 9 })
    user = user_repo.get({ "id": 5 })

    return {
        "message": "User created successfully",
        "data": user,
        "status_code": 201
    }
```


## 🧪 Writing a New Logic File for Non Resource Based Endpoints

Non resource logic files are the same as resource based logic files. except it take onely one parameter `request`.
Here’s a template to follow:

```python
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker

@enforce_request_type()
def execute(request: IRequest):
     """
    Handles the execution of business logic for a given endpoint.

    Args:
        request (IRequest): An abstracted request object that provides access to request data 
                            (e.g., JSON body, form data, files, query params) in a framework-agnostic way.
                            check domain_layer.abstractions.request_interface for all the methods
        
    Returns:
        Any: The result of the business logic execution, typically a dictionary or primitive that the caller
             serializes as an HTTP response.
    """

    # Access data
    form_data = request.get_form_data()
    json_data = request.get_json()
    path_params = request.get_path_params()

    # Use repositories
    repo_manager = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_manager.get_repo_invoker("Users")

    # Business logic
    user = user_repo.transact("POST", form_data)

    return {
        "message": "User created successfully",
        "data": user,
        "status_code": 201
    }
