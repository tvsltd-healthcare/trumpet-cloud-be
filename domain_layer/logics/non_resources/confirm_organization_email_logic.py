import time
from typing import List, Optional, Tuple

from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request):
    """
    Verifies a user token, checks if the user not exists by email, and generates a new token if not.
    
    Args:
        request: The request object containing a JSON body with a token.
    
    Returns:
        Dict containing message, status_code, and optional data.
    """
    # todo: auth: organization_type should be 'data_owner' or 'researcher'. role should be researcher_admin for researcher org / data_owner_admin for don org
    # AUTH TESTED

    body = request.get_json()
    response_formatter = ResponseFormatter()

    decode_token = token_parser(body.get("token"))

    email = decode_token.get("email")
    role = decode_token.get("role")
    organization_type = decode_token.get("organization_type")

    if not match_org_type_with_role(organization_type, role):
        return response_formatter.error("Not allowed.", 403)

    if not email:
        return response_formatter.error('Email missing.', 400)

    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")

    try:
        user = user_repo_invoker.get({"email": email}, False)
        if not user:
            auth_getter_adapter = AuthManager.get()
            token = auth_getter_adapter.generate_token(
                {"email": email, "role": role, "organization_type": organization_type})

            data = {
                "token": token.get('token'),
                'email': email,
                "role": role,
                "organization_type": organization_type,
                "expires_in": int(time.time()) + int(token["expires"])
            }

            if token:
                return response_formatter.success(data, 'User token verify successfully.', 200)
            else:
                return response_formatter.error('Failed to generate new token.', 400)
        else:
            return response_formatter.error('User already registered with this email.', 403)

    except Exception as e:
        return response_formatter.error(str(e), 500)


def match_org_type_with_role(organization_type, role) -> bool:
    if organization_type not in ('data_owner', 'researcher'):
        return False
    
    if organization_type == 'data_owner' and role not in ('data_owner_admin'):
        return False
    
    if organization_type == 'researcher' and role not in ('researcher', 'researcher_admin'):
        return False
    
    return True

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
