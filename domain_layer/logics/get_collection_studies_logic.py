import json
import re

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Retrieves a filtered collection of records based on path and query parameters.

    This function:
      1. Extracts path parameters from the request.
      2. Parses `filter` from query parameters (if provided as JSON string).
      3. Combines both into a final query object.
      4. Uses the provided repository to fetch records matching the query.
      5. Returns a formatted success response with the retrieved data.

    Args:
        request (IRequest): Abstract request object providing access to path and query parameters.
        repo: The repository interface used to fetch the collection of records.
        entity (Any, optional): Currently unused, present for interface consistency.

    Returns:
        dict: A formatted success response.

    Success Response Format:
        {
            "message": "Data retrieved successfully.",
            "status_code": 200,
            "data": [  # list of matched records
                {...}, {...}
            ]
        }
    """
    decode_token = token_parser(request.get_headers()['authorization'])
    response_formatter = ResponseFormatter()

    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    organization_users_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("OrganizationUsers")

    # Extract organization_id
    organization_user = organization_users_repo.get({"user_id": decode_token.get('user_id')}, False)
    organization_id = organization_user.get('organization_id')
    if not organization_id:
        return response_formatter.error('Organization not found', 400)

    # Step 1: Extract path and query params
    ids = request.get_path_params()
    query = request.get_query_params()
    query = query.get('filter', {}) if isinstance(query, dict) else {}

    # Step 2: Safely parse query as JSON if it's a string
    query = re.sub(r"'([^']*)'", r'"\1"', query) if query and isinstance(query, str) else query # Matches single-quoted string literals like: 'hello'

    try:
        query = json.loads(query)
    except (json.JSONDecodeError, TypeError):
        query = {}

    # Step 3: Combine path and query filters
    query = {**ids, **query, "organization_id": organization_id}

    # Step 4: Fetch records and return response
    collected_records = repo.get_collection(query)

    return response_formatter.success(
        collected_records,
        message="Data retrieved successfully.",
        status_code=200
    )
