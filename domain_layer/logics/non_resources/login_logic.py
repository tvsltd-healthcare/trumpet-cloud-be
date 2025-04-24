import anyio
import time

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
        password_handler = PasswordManager.get()
        check_password = password_handler.verify_password(body.get('password'), user.get('password'))
        if check_password:
            auth_getter_adapter = AuthManager.get()
            token = auth_getter_adapter.generate_token({"user_id": user.get('id')})
            # find user role
            role_user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("UserRoles")
            role_user_query = {
                "user_id": user['id'],
            }
            role_user = role_user_repo_invoker.get(role_user_query, False)
            # find role
            role_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Roles")
            role_query = {
                "id": role_user['role_id'],
            }
            role = role_repo_invoker.get(role_query, False)
            # success response object
            success_response_object = {
                "access_token": token['token'],
                "expires_in": (int(time.time()) + int(token['expires'])),
                "user": {
                    "first_name": user['first_name'],
                    "last_name": user['last_name'],
                    "email": user['email'],
                    "phone_number": user['phone'],
                    "role": role['name']
                }
            }
            return {
                "message": "User successfully logged in.",
                "data": success_response_object,
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
