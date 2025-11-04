import json

from datetime import datetime, timedelta, timezone
from typing import List, Optional, Tuple

from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser
from logic_injector.base_logic_injector import BaseLogicInjector

def execute(request: IRequest):
    # todo: auth: things r ok. but can chreck current user should be researcher admin or researcher
    # AUTH TESTED
    # TOKEN NEEDED

    try:
        response_formatter = ResponseFormatter()

        current_user_id, current_org_id = get_current_user_and_org_id(request)
        if not current_user_id or not current_org_id:
            return response_formatter.error("Not allowed.", 403)

        if not current_user_id or not current_org_id:
            return response_formatter.error("Not allowed.", 403)

        if not user_has_roles(current_user_id, 'researcher', 'researcher_admin'):
            return response_formatter.error("Not allowed.", 403)
        
        if not org_is_of_type(current_org_id, 'researcher'):
            return response_formatter.error("Not allowed.", 403)

        repo_discovery: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()
        dataset_repo = repo_discovery.get_repo_invoker("Datasets")
        org_repo = repo_discovery.get_repo_invoker("Organizations")
        study_agreement_repo = repo_discovery.get_repo_invoker("StudyAgreements")
        org_agreement_repo = repo_discovery.get_repo_invoker("OrganizationStudyAgreements")
        org_users_repo = repo_discovery.get_repo_invoker("OrganizationUsers")

        body = request.get_json()
        study_agreement_id = body.get('study_agreement_id')
        
        if not study_agreement_id:
            return response_formatter.error("Study agreement not found.", 403)
        
        study_agreement = study_agreement_repo.get({"id": study_agreement_id}, is_collection=False)

        if not study_agreement:
            return response_formatter.error("Study Agreement not found.", 403)

        if study_agreement.get('next_training_time'):
            if datetime.now(timezone.utc) < study_agreement['next_training_time']:
                return response_formatter.error("Training already in progress.", 403)

        study_agreement['pet_config'] = json.loads(study_agreement['pet_config'])
        
        study_agreement_status = study_agreement.get('status', None)

        if study_agreement_status != 'approved':
            return response_formatter.error("Study Agreement is not approved.", 403)

        org_id = _get_current_user_org_id(request, org_users_repo)
        if not org_id:
            return response_formatter.error("User is not assigned to any organization.", 403)
        
        organization = org_repo.get({"id": org_id}, is_collection=False)
        if not organization or organization.get("type") != "researcher":
            return response_formatter.error("Not Permitted.", 403)
        
        do_org_agreements = org_agreement_repo.get(
            {"study_agreement_id": study_agreement_id, 'organization_type': 'data_owner'},
            is_collection=True
        )

        do_study_agreement_and_dataset = [
            {
                "organization": get_organization(do_org_agreement, org_repo),
                "dataset": get_dataset(do_org_agreement, dataset_repo)
            }
            for do_org_agreement in do_org_agreements
        ]

        BaseLogicInjector().inject_business_logic(study_agreement=study_agreement, do_org_agreements=do_study_agreement_and_dataset)

        next_training_time = datetime.now(timezone.utc) + timedelta(minutes=5)

        study_agreement_repo.transact(
            method="PATCH",
            data={"next_training_time": next_training_time},
            query={"id": study_agreement_id}
        )

        study_agreement["next_training_time"] = next_training_time

        return response_formatter.success(
            message="Training Started Successfully.",
            data=study_agreement,
            status_code=202
        )
    except Exception as e:
        return response_formatter.error(f"Internal server error.", 500)

def _get_current_user_org_id(request: IRequest, org_users_repo) -> int | None:
    """Extracts the current user's organization ID using the Authorization token."""
    auth_header = request.get_headers().get("authorization")
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get("user_id")

    org_user = org_users_repo.get({"user_id": current_user_id}, is_collection=False)

    return org_user.get("organization_id") if org_user else None


def get_organization(do_org_agreement, org_repo):
    organization = org_repo.get({"id": do_org_agreement["organization_id"], "type": "data_owner"}, is_collection=False)
    return organization

def get_dataset(do_org_agreement, dataset_repo):
    dataset = dataset_repo.get({"id": do_org_agreement["dataset_id"]}, is_collection=False)
    return dataset

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
