from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type

@enforce_request_type()
def execute(request: IRequest):
    # todo: need to fix this implementation
    # todo: the request implementation should come from wrap-restify
    body = request.get_json()
    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")
    query = {
        "email": body.get("email"),
    }
    user = user_repo_invoker.get(query, False)
    if user:
        auth_getter_adapter = AuthManager.get()
        token = auth_getter_adapter.generate_token({"user_id": user.get('id')})
        return {
            "message": "User successfully logged in.",
            "data": token,
            "status_code": 200,
        }
    else:
        return {
            "message": "User not found",
            "status_code": 404,
        }
