import time

from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    """
    Generates a token for the organization of the currently authenticated user.
    This function performs the following steps:
        1. Parses the authorization token from the request headers.
        2. Extracts the user ID from the decoded token.
        3. Retrieves the organization ID associated with the user.
        4. Generates a new token for the organization using the AuthManager.
    Args:
        request (IRequest): The request object containing headers with authorization token.
    Returns:
        ResponseFormatter: A formatted response containing the generated token data.
    """
    body = request.get_json()
    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')
    if not current_user_id:
        return response_formatter.error("Invalid token. User ID not found.", 401)
    # get user organization id
    organization_user_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
    organization_user = organization_user_repo.get({"user_id": current_user_id}, False)
    if not organization_user:
        return response_formatter.error("User not found in organization.", 404)
    organization_id = organization_user.get("organization_id")
    if not organization_id:
        return response_formatter.error("Organization ID not found for user.", 404)

    # generate token for organization
    auth_manager = AuthManager.get()
    token = auth_manager.generate_token({"organization_id": organization_id, "user_id": current_user_id, "type": "DATA_OWNER_TOKEN", "expiry": body.get('expiry')})
    token_data = {
        "access_token": token["token"],
        "expires_in": int(time.time()) + int(token["expires"])
    }
    return response_formatter.success(
        data=token_data,
        message="Token generated successfully.",
        status_code=200
    )


