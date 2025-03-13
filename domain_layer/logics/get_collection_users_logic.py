from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager


def execute(query, repo):
    repo_discovery_getter_adapter:IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    org_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Organizations")
    
    query = {
        "id": 1
    }

    org = org_repo_invoker.get(query, False)

    print("This is fetched org")
    print(org)

    return "get_collection Executing GET logic for users with query: " + str(query)
