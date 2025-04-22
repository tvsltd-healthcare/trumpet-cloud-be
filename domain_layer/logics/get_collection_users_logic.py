from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager

from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type

@enforce_request_type()
def execute(request: IRequest, repo):
    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    org_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Organizations")
    
    query = request.get_path_params()

    org = org_repo_invoker.get(query, False)

    user_post_dict = {
                "first_name": "jhon",
                "last_name": "doe",
                "email": "jhon@tvs.com",
                "password": "string",
                "status": "pending",
                "phone": "01715462522"
            }
    
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")
    # user = user_repo_invoker.transact("POST", user_post_dict)
    user = user_repo_invoker.transact("PUT", user_post_dict, { "id": 1 })
    # user = user_repo_invoker.transact("DELETE", {}, { "id": 9 })
    # user = user_repo_invoker.get({ "id": 5 })

    print("This is fetched org")
    print(org)

    print("This is created user")
    print(user)

    return "get_collection Executing GET logic for users with query: " + str(query)
