import json
import re

from domain_layer.abstractions.request_interface import IRequest
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.utils.get_role import get_role_name
from domain_layer.utils.parse_token import token_parser
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.response_formatter import ResponseFormatter


@enforce_request_type()
def execute(request: IRequest, repo, entity=None):
    """
    Fetches a filtered collection of records limited to users within the same organization 
    as the currently authenticated user.

    This logic performs the following steps:
      1. Authenticates and extracts the current user from the Authorization header.
      2. Retrieves the user's organization from the OrganizationUsers repository.
      3. Fetches all user IDs belonging to the same organization.
      4. Parses query and path parameters from the request.
      5. Enforces that only records belonging to the same organization’s users are fetched.

    Args:
        request (IRequest): The request object providing access to headers, query, and path params.
        repo: The repository object responsible for fetching the collection.
        entity (Any, optional): Not used in this context but preserved for interface compatibility.

    Returns:
        Any: Formatted success or error response, depending on validation and repository results.

    Successful Response Format:
        {
            "message": str,         # Success message
            "status_code": int,     # HTTP status code (usually 200)
            "data": List[Dict]      # List of user records
        }

    Error Response Format:
        {
            "message": <str>,
            "status_code": <int>
        }
    """
    response_formatter = ResponseFormatter()

    # Step 1: Extract and decode token to get current user ID
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')

    if not current_user_id:
        return response_formatter.error("Authenticated user ID not found in token.", 401)

    # Step 2: Retrieve user's organization from OrganizationUsers repo
    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    check_user_role = get_role_name(repo_discovery_getter, current_user_id)
    check_admin_role = check_user_role.get('name')

    path_params = request.get_path_params()
    query_params = request.get_query_params()
    query_data = query_params.get('filter', {}) if isinstance(query_params, dict) else {}

    # Convert single-quoted JSON to double-quoted
    if query_data and isinstance(query_data, str):
        query_data = re.sub(r"'([^']*)'", r'"\1"', query_data)

    # Parse JSON safely
    try:
        query_data = json.loads(query_data)
    except (json.JSONDecodeError, TypeError):
        query_data = {}

    final_query = {**path_params, **query_data}

    if check_admin_role != "trumpet_admin":
        organization_users_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("OrganizationUsers")

        organization_user = organization_users_repo.get({"user_id": current_user_id})
        if not organization_user:
            return response_formatter.error("User is not assigned to any organization.", 403)

        current_users_organization_id = organization_user.get('organization_id')
        if not current_users_organization_id:
            return response_formatter.error("User has no organization ID assigned.", 403)

        # Get all users in the same organization
        same_org_user_records = organization_users_repo.get({"organization_id": current_users_organization_id},
            is_collection=True)
        same_org_user_ids = [item['user_id'] for item in same_org_user_records]
        final_query['id'] = same_org_user_ids

    # Step 3: Fetch records
    collected_records = repo.get_collection(final_query)

    if not collected_records:
        return response_formatter.error("No users found in the same organization.", 404)

    # Step 6: return users role in the collection
    updated_collection = []
    for record in collected_records:
        if record.get('status') != "deleted":
            get_user_role = get_role_name(repo_discovery_getter, record.get('id'))
            if get_user_role:
                record['role'] = get_user_role.get('name')
            else:
                record['role'] = None
            updated_collection.append(record)

    return response_formatter.success(updated_collection, message="Users retrieved successfully.", status_code=200)
