import json
import re

from application_layer.abstractions.fga_authorizer_interface import IFGAAuthorizer
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.authorization_manager import AuthorizationManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.authorization import get_user_id, is_supper_admin
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.utils.parse_token import token_parser


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
        int(path_params.get("id"))
    except ValueError:
        return response_formatter.error(
            message=f"Invalid organization ID",
            status_code=400
        )

    organization_id = path_params.get("id")

    if not check_permission(request, organization_id):
        return response_formatter.error("Not allowed.", 403)

    query = request.get_query_params()
    query = query.get('filter', {}) if isinstance(query, dict) else {}

    query = re.sub(r"'([^']*)'", r'"\1"', query) if query and isinstance(query,
                                                                         str) else query  # Matches single-quoted string literals like: 'hello'
    try:
        query = json.loads(query)
    except (json.JSONDecodeError, TypeError):
        query = {}

    query = {**path_params, **query}

    collected_records = repo.get(query)
    if not collected_records:
        return response_formatter.error(message="Organization not found.",status_code=404)

    try:
        repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

        files_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Files")

        files = [file for file in files_repo.get({'organization_id': collected_records['id']}, is_collection=True)]

        collected_records['files'] = files

    except Exception as e:
        return response_formatter.error("Internal Server Error: Unable to retrieve files.")

    return response_formatter.success(
        collected_records,
        message="Data retrieved successfully.",
        status_code=200
    )

def check_permission(request: IRequest, organization_id: int):
    current_user_id = get_user_id(request)

    if is_supper_admin(current_user_id):
        return True

    authorization_handler: IFGAAuthorizer = AuthorizationManager.get()

    permision = authorization_handler.check({
            "user_type": "user",
            "user_id": current_user_id,
            "action": "get",
            "resource_type": "organization",
            "resource_id": organization_id,
        })

    return permision.get('allowed')
