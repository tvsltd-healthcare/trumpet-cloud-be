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
        organization_ids = created_agreement.get('participants', '')
        organization_ids = organization_ids.split(",")

        organization_study_agreement_repo: IAppRepoInvoker = repo_discovery_service.get_repo_invoker(
            "OrganizationStudyAgreements"
        )

        # Step 2: Link all participant organizations (pending)
        _assign_participant_organizations(
            repo=organization_study_agreement_repo,
            organization_ids=organization_ids,
            study_agreement_id=study_agreement_id
        )

        # Step 3: Get researcher's organization
        current_users_organization_id = _get_current_user_org_id(request, repo_discovery_service)
        if not current_users_organization_id:
            return response_formatter.error("User has no organization ID assigned.", 403)

        # Step 4: Link researcher's organization (approved)
        _assign_organization_to_agreement(
            repo=organization_study_agreement_repo,
            organization_id=current_users_organization_id,
            study_agreement_id=study_agreement_id,
            status="approved"
        )

        return response_formatter.success(
            created_agreement,
            message="Study agreement created and organizations assigned.",
            status_code=201
        )

    except Exception as e:
        return response_formatter.error(f"Internal server error: {str(e)}", 500)


# -------------------
# 🔒 Private Helpers
# -------------------

def _assign_participant_organizations(repo: IAppRepoInvoker, organization_ids: list, study_agreement_id: int):
    """Assigns all participant organizations with 'pending' status to the agreement."""
    for org_id in organization_ids:
        _assign_organization_to_agreement(repo, org_id, study_agreement_id, status="pending")


def _assign_organization_to_agreement(repo: IAppRepoInvoker, organization_id: int, study_agreement_id: int, status: str):
    """Helper to link an organization to a study agreement with given status."""
    data = {
        'organization_id': organization_id,
        'study_agreement_id': study_agreement_id,
        'status': status
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
g