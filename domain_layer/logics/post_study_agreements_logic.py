import json

from domain_layer.abstractions.request_interface import IRequest
from domain_layer.abstractions.app_repo_discovery_getter_interface import IAppRepoDiscoveryGetter
from domain_layer.abstractions.app_repo_invoker_interface import IAppRepoInvoker
from domain_layer.repo_discovery_manager import RepoDiscoveryManager
from domain_layer.response_formatter import ResponseFormatter
from domain_layer.utils.parse_token import token_parser


def execute(request: IRequest, repo, entity=None):
    """
    Creates a study agreement and associates it with participating organizations,
    including the researcher's own organization.

    This function performs the following:
    1. Creates a new study agreement using the provided `repo` and request path/entity.
    2. Associates each participant organization (from the 'participants' field) with the agreement.
    3. Extracts the user from the Authorization token.
    4. Finds the researcher's organization and also links it to the agreement as 'approved'.

    Args:
        request (IRequest): The request object providing access to headers and path params.
        repo: Repository interface to handle the creation of the study agreement.
        entity (dict, optional): Data to create the study agreement.

    Returns:
        dict: Success or error response formatted using ResponseFormatter.
    """
    response_formatter = ResponseFormatter()
    repo_discovery_service: IAppRepoDiscoveryGetter = RepoDiscoveryManager.get()

    try:
        # Step 1: Create the study agreement
        ids = request.get_path_params()
        created_agreement = repo.post(entity, ids)

        study_agreement_id = created_agreement.get('id')

        if not created_agreement.get('datasets'):
            return response_formatter.error("No datasets provided.", 400)
        
        dataset_ids = created_agreement.get('datasets', '').split(",")
        datasets = _get_datasets(repo_discovery_service, dataset_ids)

        if not datasets:
            return response_formatter.error("No datasets provided.", 400)
        
        agreement_use_case = created_agreement.get('use_case')

        if not agreement_use_case:
            return response_formatter.error("No use case provided for agreement.", 400)

        if not _validate_unique_organization_ids(datasets):
            return response_formatter.error("Some of the selected datasets are from the same organization.", 400)
        
        if not _validate_use_cases(datasets, agreement_use_case):
            return response_formatter.error("Each dataset's use case should match the agreement's use case.", 400)
        
        # Get researcher's organization
        current_users_organization_id = _get_current_user_org_id(request, repo_discovery_service)
        if not current_users_organization_id:
            return response_formatter.error("User has no organization ID assigned.", 403)
        
        organization_study_agreement_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker(
            "OrganizationStudyAgreements"
        )

        # Link DON orgs and datasets with strudy agreement
        _assign_participant_organizations(
            repo=organization_study_agreement_repo,
            datasets=datasets,
            study_agreement_id=study_agreement_id
        )

        # Link researcher's organization (pending)
        _assign_organization_to_agreement(
            repo=organization_study_agreement_repo,
            organization_id=current_users_organization_id,
            study_agreement_id=study_agreement_id,
            organization_type="researcher"
        )

        created_agreement['pet_config'] = json.loads(created_agreement['pet_config'])
        
        return response_formatter.success(
            created_agreement,
            message="Study agreement created and organizations assigned.",
            status_code=201
        )
    except Exception as e:
        return response_formatter.error(f"Internal server error: {str(e)}", 500)


# -------------------
# Private Helpers
# -------------------

def _validate_unique_organization_ids(datasets):
    seen = set()
    for dataset in datasets:
        org_id = dataset.get("organization_id")
        if org_id in seen:
            return False 
        seen.add(org_id)
    return True

def _validate_use_cases(datasets, agreement_use_case):
    return all(dataset.get("use_case") == agreement_use_case for dataset in datasets)

def _get_datasets(repo_discovery_service, dataset_ids):
    dataset_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("Datasets")
    return dataset_repo.get({'id': dataset_ids}, is_collection=True)


def _assign_participant_organizations(repo: IAppRepoInvoker, datasets: list, study_agreement_id: int):
    """Assigns all participant organizations with 'pending' status to the agreement."""
    for dataset in datasets:
        _assign_organization_to_agreement(repo, dataset['organization_id'], study_agreement_id, organization_type="data_owner", dataset_id=dataset['id'])


def _assign_organization_to_agreement(repo: IAppRepoInvoker, organization_id: int, study_agreement_id: int, organization_type: str, dataset_id: int = None):
    """Helper to link an organization to a study agreement with given status."""
    data = {
        'organization_id': organization_id,
        'study_agreement_id': study_agreement_id,
        'dataset_id': dataset_id,
        'organization_type': organization_type
    }
    repo.transact("POST", data=data)


def _get_current_user_org_id(request: IRequest, repo_discovery_service: IAppRepoDiscoveryGetter) -> int | None:
    """Extracts the current user's organization ID from token and organization_users repo."""
    auth_header = request.get_headers().get('authorization')
    decoded_token = token_parser(auth_header)
    current_user_id = decoded_token.get('user_id')

    organization_users_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker("OrganizationUsers")
    organization_user = organization_users_repo.get({"user_id": current_user_id})

    return organization_user.get('organization_id') if organization_user else None
