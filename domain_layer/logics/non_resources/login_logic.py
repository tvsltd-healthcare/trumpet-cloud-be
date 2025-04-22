import anyio

from adapters.password_adapters.bcrypt_adapters import PasswordHandler
from application_layer.abstractions.password_manager_interface import IPasswordManager
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.auth_manager import AuthManager
from domain_layer.password_manager import PasswordManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager


def execute(request):
    # todo: need to fix this implementation
    # todo: the request implementation should come from wrap-restify
    body = anyio.from_thread.run(request.json)
    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")
    query = {
        "email": body.get("email"),
    }
    user = user_repo_invoker.get(query, False)
    if user:
        # check password
        password_manager = PasswordManager.get()
        check_password = password_manager.verify_password(body.get('password'), user.get('password'))
        if check_password:
            auth_getter_adapter = AuthManager.get()
            token = auth_getter_adapter.generate_token({"user_id": user.get('id')})
            return {
                "message": "User successfully logged in.",
                "data": token,
                "status_code": 200,
            }
        else:
            return {
                "message": "Invalid password.",
                "status_code": 404,
            }
    else:
        return {
            "message": "User not found",
            "status_code": 404,
        }
