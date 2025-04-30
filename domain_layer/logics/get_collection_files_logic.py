import json

from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type

@enforce_request_type()
def execute(request: IRequest, repo, entity = None):
    print('into loginc -----')
    ids = request.get_path_params()
    
    query = request.get_query_params()
    query = query.get('filter', {}) if isinstance(query, dict) else {}

    try:
        query = json.loads(query)
    except (json.JSONDecodeError, TypeError):
        query = {}
    
    query = {**ids, **query}
    return repo.get_collection(query)
