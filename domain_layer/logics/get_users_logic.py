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

    try:
        path_params = request.get_path_params()
    except KeyError:
        return response_formatter.error(
            message="Path parameters are missing in the request.",
            status_code=400
        )

    try:
        user_id  = int(path_params.get("id"))
    except ValueError:
        return response_formatter.error(
            message=f"Invalid user ID",
            status_code=400
        )

    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Users")

    user = user_repo.get({"id": user_id})
    if not user:
        return response_formatter.error(message="User not found.",status_code=404)

    get_user_role = get_role_name(repo_discovery_getter, path_params.get("id"))
    if not get_user_role:
        return response_formatter.error("User role not found.", 404)
    user["role"] = get_user_role.get("name")

    return response_formatter.success(
        user,
        message="Users retrieved successfully.",
        status_code=200
    )

