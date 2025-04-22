from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type

@enforce_request_type()
def execute(request: IRequest):
    #get roles repo
    #roles_repo = RepoDiscovery.ge("Roles")
    #roles.repo.create(role: )
    # print("logic req", request)
    # print("logic req url====", request.get_request())
    print("logic req files====")
    print(request.get_files())
    
    return {"logic_res": "Executing GET logic for users with query: "}
