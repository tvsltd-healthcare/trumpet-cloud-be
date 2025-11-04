import time
from typing import List, Optional, Tuple

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
    This token will be used by data owner to communicate with cloud.
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
    # todo: auth: we may chk user role to be data owner to make it concrete
    # AUTH TESTED
    # TOKEN NEEDED

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
    
    if not org_is_of_type(organization_id, 'data_owner'):
        return response_formatter.error("Not allowed.", 403)
    
    if not user_has_roles(current_user_id, 'trumpet_admin', 'data_owner_admin'):
        return ResponseFormatter().error("Not allowed.", 403)

    # check if organization is approved
    organization_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Organizations")
    organizations = organization_repo.get({"id": organization_id}, False)
    if organizations.get("status") != "approved":
        return response_formatter.error("Organization is not approved.", 403)

    if organizations.get('type') != "data_owner":
        return response_formatter.error("Only data owner organizations can generate tokens.", 403)

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


###### COMMON AUTHN METHODS #########

def get_current_user_and_org_id(
    request: IRequest,
) -> Optional[Tuple[int, int]]:
    """
    Extract the current user's ID and organization ID from the JWT token in the Authorization header.

    Args:
        request: The incoming request object, providing access to headers.

    Returns:
        A tuple of (user_id, organization_id) if found, otherwise None.
    """
    # Extract Authorization header
    auth_header = request.get_headers().get("authorization")
    if not auth_header:
        return None, None
    

    # Decode JWT and extract user_id
    try:
        decoded_token = token_parser(auth_header)
    except Exception as e:
        return None, None
    
    user_id = decoded_token.get("user_id")
    if not user_id:
        return None, None

    # Lookup organization_id from repository
    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    org_users_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("OrganizationUsers")
    org_user = org_users_repo.get({"user_id": user_id})

    if not org_user:
        return None, None

    org_id = org_user.get("organization_id")
    if not org_id:
        return None, None

    return user_id, org_id


def get_role_names_from_user_id(user_id: int) -> List[str]:
    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    user_roles_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("UserRoles")
    user_roles = user_roles_repo.get({"user_id": user_id}, is_collection=True)

    role_ids = [user_role.get("role_id") for user_role in user_roles]

    roles_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Roles")
    roles = roles_repo.get({"id": role_ids}, is_collection=True)

    role_names = [role.get("name") for role in roles]
    return role_names


def user_has_roles(user_id: int, *allowed_roles: str) -> bool:
    """Return False if the current organization type is not allowed."""
    user_role_names = get_role_names_from_user_id(user_id)

    if not user_role_names:
        return False
    
    return any(role in allowed_roles for role in user_role_names)


def user_belongs_to_the_org(user_id: int, org_id: int) -> bool:
    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    org_users_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("OrganizationUsers")
    org_user = org_users_repo.get({"user_id": user_id})
    return str(org_user.get('organization_id')) == str(org_id)


def user_has_access_to_target_org(target_org_id: int, current_user_id: int, current_org_id: int) -> bool:
    if user_has_roles(current_user_id, 'trumpet_admin'):
        return True
    
    return str(target_org_id) == str(current_org_id)


def org_is_of_type(organization_id: int, *allowed_types: str) -> bool:
    """Return False if the current organization type is not allowed."""
    organization = get_org_from_id(organization_id)

    if not organization:
        return False
    
    return (organization.get('type') in allowed_types)


def get_org_from_id(org_id: int):
    repo_discovery_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    organization_repo: IAppRepoInvoker = repo_discovery_getter.get_repo_invoker("Organizations")
    return organization_repo.get({'id': org_id}, is_collection=False)
