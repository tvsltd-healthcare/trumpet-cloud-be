from typing import List, Optional, Tuple
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest):
    """
    Updates the status of a study agreement for the requesting user's organization.
    If all associated organization agreements are approved, the overall study agreement
    is marked as approved.

    Workflow:
    1. Extracts and validates required request data.
    2. Verifies that the study agreement and the organization-specific agreement exist.
    3. Updates the organization's agreement status.
    4. If all org agreements for the study are approved, marks the overall study agreement as approved.

    Args:
        request (IRequest): Request object containing JSON body, headers, and context.

    Returns:
        dict: A formatted response from ResponseFormatter with either:
            - success: containing updated organization agreement info
            - error: with appropriate HTTP status and message
    """
    # todo: auth: things r ok. but can chreck current user should be data owner and org shoukd be don type
    # AUTH TESTED
    # TOKEN NEEDED

    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    current_user_id, current_org_id = get_current_user_and_org_id(request)
    if not current_user_id or not current_org_id:
        return response_formatter.error("Not allowed.", 403)

    if not user_has_roles(current_user_id, 'data_owner_admin'):
        return response_formatter.error("Not allowed.", 403)
    
    if not org_is_of_type(current_org_id, 'data_owner'):
        return response_formatter.error("Not allowed.", 403)

    try:
        # Step 1: Get current user's organization ID
        org_id = _get_current_user_org_id(request, repo_discovery_service)
        if not org_id:
            return response_formatter.error("User is not assigned to any organization.", 403)

        # Step 2: Parse and validate request body
        body = request.get_json()
        study_agreement_id = body.get('study_agreement_id')
        status = body.get('status')

        if not study_agreement_id or not status:
            return response_formatter.error("Both 'study_agreement_id' and 'status' are required.", 400)

        # Step 3: Verify study agreement exists
        study_agreement_repo = repo_discovery_service.get_repo_invoker("StudyAgreements")
        study_agreement = study_agreement_repo.get({'id': study_agreement_id})
        if not study_agreement:
            return response_formatter.error("Study agreement not found.", 404)

        # Step 4: Get and update org-specific agreement
        org_agreement_repo = repo_discovery_service.get_repo_invoker("OrganizationStudyAgreements")
        org_agreement_query = {
            'study_agreement_id': study_agreement_id,
            'organization_id': org_id
        }

        org_agreement = org_agreement_repo.get(org_agreement_query)
        if not org_agreement:
            return response_formatter.error("Study agreement not found for this organization.", 404)

        updated_org_agreement = org_agreement_repo.transact(
            "PATCH",
            data={'status': status},
            query=org_agreement_query
        )

        # Step 5: Check if all org agreements are approved
        all_do_org_agreements = org_agreement_repo.get(
            {'study_agreement_id': study_agreement_id, 'organization_type': 'data_owner'},
            is_collection=True
        )

        if _are_all_org_agreements_approved(all_do_org_agreements):
            org_agreement_repo.transact(
                "PATCH",
                data={'status': 'approved'},
                query={'study_agreement_id': study_agreement_id, 'organization_type': 'researcher'}
            )
            
            study_agreement_repo.transact(
                "PATCH",
                data={'status': 'approved'},
                query={'id': study_agreement_id}
            )

        return response_formatter.success(
            updated_org_agreement,
            message="Organization study agreement status updated successfully.",
            status_code=200
        )

    except Exception as e:
        return response_formatter.error(f"Internal server error: {str(e)}", 500)


# -------------------
# Private Helpers
# -------------------

def _get_current_user_org_id(request: IRequest, repo_discovery_service: IAppRepoDiscoveryGetter) -> int | None:
    """Extracts the current user's organization ID using their token."""
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')

    organization_users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
    organization_user = organization_users_repo.get({"user_id": current_user_id})

    return organization_user.get('organization_id') if organization_user else None


def _are_all_org_agreements_approved(agreements: list[dict]) -> bool:
    """Returns True if all organization agreements have status 'approved'."""
    return all(item.get("status") == "approved" for item in agreements)


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
