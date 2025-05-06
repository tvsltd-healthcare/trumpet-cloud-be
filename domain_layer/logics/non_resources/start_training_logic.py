import json
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    """
    Retrieves all study agreements associated with the current user's organization,
    filtered by optional status or other query parameters.

    Steps:
    1. Identify the current user's organization using the token.
    2. Parse and validate optional query filters (e.g., status).
    3. Fetch organization-study-agreements for the user's org.
    4. Fetch and return corresponding study agreements if any.

    Args:
        request (IRequest): The incoming request containing headers and optional query parameters.

    Returns:
        dict: Formatted response with a list of matched study agreements, or error details.
    """
    pass


# -------------------
# Private Helpers
# -------------------

def _get_current_user_org_id(request: IRequest, repo_discovery_service: IAppRepoDiscoveryGetter) -> int | None:
    """Extracts the current user's organization ID using the JWT token in the Authorization header."""
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')

    organization_users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
    organization_user = organization_users_repo.get({"user_id": current_user_id})

    return organization_user.get('organization_id') if organization_user else None

