import json
import re

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Executes the main application workflow to process a given request by interacting
    with the provided repository and optionally an entity. The process involves extracting
    path and query parameters, parsing them safely, fetching related records from the
    repository, and subsequently interacting with an additional "Files" repository to
    enrich the records with file details.

    Args:
        request (IRequest): The request object containing path and query parameters.
        repo: The primary repository interface used for querying data.
        entity (optional): Additional entity context for execution.

    Returns:
        Dict: A formatted response containing the retrieved data or an error message.
    """
    response_formatter = ResponseFormatter()

    # Step 1: Extract path and query params
    ids = request.get_path_params()
    query = request.get_query_params()
    query = query.get('filter', {}) if isinstance(query, dict) else {}

    # Step 2: Safely parse query as JSON if it's a string
    query = re.sub(r"'([^']*)'", r'"\1"', query) if query and isinstance(query,
                                                                         str) else query  # Matches single-quoted string literals like: 'hello'

    try:
        query = json.loads(query)
    except (json.JSONDecodeError, TypeError):
        query = {}

    # Step 3: Combine path and query filters
    query = {**ids, **query}

    # Step 4: Fetch records and return response
    collected_records = repo.get(query)

    print(f"{collected_records}")

    try:
        repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

        files_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Files")
        print(f"{files_repo}")

        files = [{
            'id': file.get('id'),
            'name': file.get('filename')
        } for file in files_repo.get({'organization_id': collected_records['id']}, is_collection=True)]

        collected_records['files'] = files

    except Exception as e:
        print(f"Error: {e}")
        return response_formatter.error("Internal Server Error: Unable to retrieve files.")

    return response_formatter.success(
        collected_records,
        message="Data retrieved successfully.",
        status_code=200
    )
