import json
import re

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.response_formatter import ResponseFormatter


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
    response_formatter = ResponseFormatter()
    ids = request.get_path_params()
    # initialize repo discovery manager
    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    # get the repo invoker for the specified repo
    organization_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Organizations")
    organization = organization_repo.get({"id": ids.get("organization_id")}, False)
    if not organization:
        return response_formatter.error('Organization not found', 404)

    # get the repo invoker for the specified repo
    organization_users_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("OrganizationUsers")
    organization_users = organization_users_repo.get({"organization_id": organization.get("id")}, True)
    if not organization_users:
        return response_formatter.error('Organization users not found', 404)

    # get the repo invoker for the specified repo
    user_info = []
    for user in organization_users:
        users_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Users")
        user_data = users_repo.get({"id": user.get("user_id")}, False)
        if not user_data:
            return response_formatter.error('User not found', 404)
        # append user data to user info list
        user_list = {
            "id": user_data.get("id"),
            "first_name": user_data.get("first_name"),
            "last_name": user_data.get("last_name"),
            "email": user_data.get("email"),
            "status": user_data.get("status"),
            "phone": user_data.get("phone"),
        }
        user_info.append(user_list)
    organization["users"] = user_info
    return {
        "message": "Data retrieved successfully.",
        "status_code": 200,
        "data": organization
    }

