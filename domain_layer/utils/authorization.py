from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.parse_token import token_parser



def is_supper_admin(user_id):
    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    role_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Roles")
    role_user_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("UserRoles")

    user_role = role_user_repo.get({"user_id": user_id})
    role = role_repo.get({"id": user_role.get("role_id")})

    print(f"{user_id=}")
    print(f"{role=}")

    if role.get("name") == "trumpet_admin":
        return True
    return False

def get_user_id(request: IRequest):
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    return decoded_token.get('user_id')