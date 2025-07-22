from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker


def get_users(repo_discovery_getter: IAppRepoDiscoveryGetter, user_ids: list[str] | str) -> list[dict]:
    """
    Retrieve user details for a list of user IDs.

    Args:
        repo_discovery_getter (IAppRepoDiscoveryGetter): The repository discovery getter instance.
        user_ids (list[str]): A list of user IDs to retrieve.

    Returns:
        list[dict]: A list of user details dictionaries.
    """
    if not user_ids:
        return []

    user_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Users")
    if isinstance(user_ids, str):
        user_ids = [user_ids]
    users = user_repo.get({"id": user_ids}, True)
    return users if isinstance(users, list) else [users] if users else []
