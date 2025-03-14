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

    user_post_dict = {
        "first_name": "khal",
        "last_name": "imr",
        "email": "abc@tvs.com",
        "password": "string",
        "status": "pending",
        "phone": "01715462534"
        }
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")
    user = user_repo_invoker.transact("POST", user_post_dict)

    print("This is fetched org")
    print(org)

    print("This is created user")
    print(user)

    return "get_collection Executing GET logic for users with query: " + str(query)
