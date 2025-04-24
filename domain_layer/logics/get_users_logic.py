from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type

@enforce_request_type()
def execute(request: IRequest, repo, entity = None):
    return "Executing GET logic for users with query: "
