from typing import List, Optional, Tuple
from fastapi import HTTPException

from adapters.middlewares.auth_middleware import AuthMiddleware
from domain_layer.auth_manager import AuthManager
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.dependency.email_service_manager import EmailServiceManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.enforce_request_interface import enforce_request_type
from domain_layer.utils.parse_token import token_parser

@enforce_request_type()
def execute(request: IRequest):
    """
    Handles the "forgot password" or invitation flow by checking if a user exists.
    If the user does not exist, generates a token and sends it via email.

    This method:
    1. Retrieves the email from the request body.
    2. Checks if a user already exists with the given email.
    3. If not, generates a token and sends an email using the configured email service.
    4. If the user already exists, returns an error indicating duplication.

    Args:
        request (IRequest): An object implementing the IRequest interface containing the JSON body.

    Returns:
        dict: A formatted response from ResponseFormatter.
              - Success: Indicates the email has been sent with a 200 status code.
              - Error: If the user already exists or email sending fails, returns a 500 error.

    Raises:
        Exception: Any issues during email generation or sending are caught and returned as 500 error.

    Example:
        ```python
        request = Request(json={"email": "john@example.com"})
        result = execute(request)
        # If user doesn't exist: {"status": "success", "message": "Successfully email send.", "data": {}}
        # If user exists: {"status": "error", "message": "User already registered with this email.", ...}
        ```
    """
    # todo: auth: current user should be researcher admin; also may cross chk the org should be of type researcher
    # AUTH TESTED
    # TOKEN NEEDED

    response_formatter = ResponseFormatter()

    current_user_id, current_org_id = get_current_user_and_org_id(request)
    if not current_user_id or not current_org_id:
        return response_formatter.error("Not allowed.", 403)

    if not user_has_roles(current_user_id, 'researcher_admin'):
        return response_formatter.error("Not allowed.", 403)
    
    if not org_is_of_type(current_org_id, 'researcher'):
        return response_formatter.error("Not allowed.", 403)

    body = request.get_json()

    email = body.get("email")
    if not email:
        return response_formatter.error('Email field is required.', 400)
    email = email.strip().lower()

    organization_id = body.get("organization_id")
    if not organization_id:
        return response_formatter.error('Organization id field is required.', 400)
    
    if str(organization_id) != str(current_org_id):
        return response_formatter.error("Not allowed.", 403)

    query = {"email": email}
    role = "researcher"

    repo_discovery_getter_adapter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo_invoker: IAppRepoInvoker = repo_discovery_getter_adapter.get_repo_invoker("Users")

    try:
        user = user_repo_invoker.get(query, False)

        if not user:
            auth_getter_adapter = AuthManager.get()
            token = auth_getter_adapter.generate_token({
                "email": email, "role": role, "organization_id": organization_id})

            token_value = token["token"] if isinstance(token, dict) else token

            email_service = EmailServiceManager.get()
            email_service.send_email(email, token_value, type='varify_researcher')
            return response_formatter.success( {}, 'Successfully email send.', 200)
        else:
            return response_formatter.error('User already registered with this email.', 500)

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
