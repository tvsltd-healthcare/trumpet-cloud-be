from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager

def execute(entity, query, repo):

    create_user = repo.post(entity, query)
    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    organization_users_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("OrganizationUsers")

    organization_users = {
        "user_id": create_user.get("id"),
        "organization_id": 16
    }
    organization_users_create = organization_users_repo_invoker.transact("POST", data =organization_users)

    return organization_users_create