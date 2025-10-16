from typing import List, Optional, Tuple
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.authorization_manager import AuthorizationManager
from domain_layer.password_manager import PasswordManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    # todo: auth: organization type should be researcher
    # AUTH TESTED

    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Users")
    password_handler = PasswordManager.get()

    body = request.get_json()

    decode_token = token_parser(request.get_headers()['authorization'])

    email = decode_token.get("email")
    if not email:
        return response_formatter.error('Email missing.', 400)

    organization_id = decode_token.get("organization_id")
    if organization_id is None:
        return response_formatter.error('Organization missing.', 400)
    
    if not org_is_of_type(organization_id, 'researcher'):
        return response_formatter.error("Not allowed.", 403)

    phone = body.get("phone")
    if user_repo.get({"phone": phone}, is_collection=False):
        return response_formatter.error('Phone number already registered.', 400)

    role_name = "researcher"

    try:
        user = {
            "first_name": body.get("first_name"),
            "last_name": body.get("last_name"),
            'email': email,
            'phone': body.get("phone"),
            'password': password_handler.hash_password(body.get("password")),
        }
        created_user = user_repo.transact("POST", data=user)
        if not created_user:
            return response_formatter.error('User creation failed: Invalid or empty response from users.', 500)
        created_user.pop("password", None)

        organization_users = {
            "user_id": created_user.get("id"),
            "organization_id": organization_id
        }
        organization_users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
        user_assign_to_organization = organization_users_repo.transact("POST", data=organization_users)
        if not user_assign_to_organization:
            return response_formatter.error(
                'Failed to assign user to organization: Invalid response from organization user', 500)

        role_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Roles")
        role = role_repo.get({"name": role_name})
        if not role:
            return response_formatter.error('Role retrieval failed: Invalid or empty response from roles', 500)

        role_user = {
            "user_id": created_user.get("id"),
            "role_id": role.get("id")
        }
        role_user_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("UserRoles")
        role_user_repo.transact("POST", data=role_user)
        if not created_user:
            return response_formatter.error('User creation failed: Invalid or empty response from users.', 500)

        authorization_handler = AuthorizationManager.get()

        authorization_handler.add_relation({
            "user_type": "user",
            "user_id": user_assign_to_organization.get("user_id"),
            "action": "owner",
            "resource_type": "user",
            "resource_id": user_assign_to_organization.get("user_id"),
        })

        authorization_handler.add_relation({
            "user_type": "user",
            "user_id": user_assign_to_organization.get("user_id"),
            "action": "researcher",
            "resource_type": "organization",
            "resource_id": user_assign_to_organization.get("organization_id"),
        })

        authorization_handler.add_relation({
            "user_type": "organization",
            "user_id": user_assign_to_organization.get("organization_id"),
            "action": "organization",
            "resource_type": "user",
            "resource_id": user_assign_to_organization.get("user_id"),
        })

        return response_formatter.success(created_user, 'User created successfully.', 201)

    except Exception as e:
        return response_formatter.error(str(e), 500)


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
