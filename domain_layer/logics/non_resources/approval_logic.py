from typing import List, Optional, Tuple
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.dependency.email_service_manager import EmailServiceManager
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.utils.parse_token import token_parser

def execute(request: IRequest):
    """
    Approves a user's status and sends a verification email.

    This function handles an incoming request to approve a user's status
    by updating their record in the database. After a successful update,
    it sends an email notification to the user. The request must contain
    a valid JSON body with the user's ID.

    Args:
        request (IRequest): The incoming HTTP request object which must
            include a JSON body with a `user_id` key.

    Returns:
        dict: A formatted response containing the result of the operation.
            - Returns 400 if the request body is missing or malformed.
            - Returns 400 if the user is not found.
            - Returns 201 if the user is successfully updated and email is sent.
            - Returns 500 in case of any internal errors during processing.
    """
    # todo: auth: the request should be from superadmin, (but can it be researcher_admin??? ask sakib bhai or prince bhai to check fronendt code)
    # if it is for both admin user and researcher then we have to cehck the trget user and token user both

    current_user_id, current_org_id = get_current_user_and_org_id(request)
    if not current_user_id or not current_org_id:
        return ResponseFormatter().error("Not allowed.", 403)
    
    if not user_has_roles(current_user_id, 'researcher_admin'):
        return ResponseFormatter().error("Not allowed.", 403)
    
    body = request.get_json()

    user_id = body.get('user_id')
    status = body.get('status')

    if not user_belongs_to_the_org(user_id, current_org_id):
        return ResponseFormatter().error("Not allowed.", 403)
    
    if not user_id or not status:
        return ResponseFormatter().error("Unprocessable Entity.", 422)

    repo_getter: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
    user_repo: IAppRepoInvoker = repo_getter.get_repo_invoker("Users")


    user = user_repo.get({'id': user_id}, False)

    if not user:
        return ResponseFormatter().error("User does not exists.", 404)

    try:
        user_status_update = user_repo.transact( "PATCH", data={'status': status}, query={'id': user.get('id')})
    except Exception as e:
        return ResponseFormatter().error(str(e), 500)

    email_service = EmailServiceManager.get()
    email_body = f"Hello, your token is"

    status = user_status_update.get('status', '').strip().lower()
    if status == 'approved':
        email_service.send_email(user.get('email'), email_body, type='approved_registration')
    elif status == 'disapproved':
        email_service.send_email(user.get('email'), email_body, type='disapproved_registration')
    else:
        return

    return ResponseFormatter().success({}, 'User status has been updated successfully.', 200)

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
