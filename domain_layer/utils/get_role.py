from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker


def get_role_name(repo_discovery_getter: IAppRepoDiscoveryGetter, user_id: str) -> None | object | list[object]:
    """
    Get the role name of a user based on their user ID.

    Args:
        repo_discovery_getter: An instance of IAppRepoDiscoveryGetter to access repositories.
        user_id (str): The ID of the user.

    Returns:
        str: The role name of the user.
    """
    user_role_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("UserRoles")
    user_role = user_role_repo.get({"user_id": user_id})
    if not user_role:
        return None

    role_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Roles")
    role = role_repo.get({"id": user_role.get("role_id")})
    if not role:
        return None

    return role



